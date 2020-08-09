from __future__ import print_function
import io
import warnings
import textwrap
from pathlib import Path
import pickle
import os.path
import google
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

import pandas as pd
from googleAPI.drive import *


class GoogleSheet(GoogleDrive):
    '''
    The base class of Google Sheet API.
    
    It aims at dealing with the Google Sheet data extract and append.
    It is not tied to a specific spreadsheet.
    
    This class is powered by pandas. Thus, make sure the data in the
    spreadsheet is able to be processed by pandas.
    
    Terminology:
      Spreadsheet: The whole file. Same level as an Microsoft Excel file.
      Sheet: A tab inside the spreadsheet. Same as Excel sheet.
    '''
    def __init__(self,
                 creds=None,
                 credential_path='',
                 credential_scopes=['https://www.googleapis.com/auth/drive'],
                 token_prefix='GoogleDrive_',
                 token_suffix=''):
        '''
        Initialize the credential.
        
        If credential `creds` is provided, this method will use it directly 
        if it is valid.
        
        Otherwise, it will use `credential_path` and `credential_scopes` to
        get the token.
        
        Args:
          creds: None or google.oauth2.credentials.Credentials, default None
          credential_path: String, default ''
            Path to the credential with either 'token.pickle' or
            'credentials.json' in it.
          credential_scopes: List of strings, default ['https://www.googleapis.com/auth/drive']
            Scope of the credential. Default scope can
            'See, edit, create, and delete all of your Google Drive files'.
            Details:
            https://developers.google.com/identity/protocols/oauth2/scopes#sheets
          token_prefix: String, default 'GoogleDrive_'
            Prefix of token file. eg. '{token_prefix}token.pickle'.
          token_suffix: String, default ''
            Suffix of token file. eg. 'token{token_suffix}.pickle'.
        '''
        if creds is not None and self.credential_validation(creds):
            self.creds = creds
        else:
            self.creds = self.credential(credential_path, credential_scopes,
                                         token_prefix, token_suffix)

    def create_spreadsheet(self, spreadsheet_name: str):
        '''
        Creates a spreadsheet, returning the newly created spreadsheet's ID.
        
        Official API guide:
        https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/create
        
        Args:
          spreadsheet_name: String
            The name of the spreadsheet.
            
        Return:
          spreadsheet ID: String
        '''
        service = build('sheets', 'v4', credentials=self.creds)
        spreadsheet = {'properties': {'title': spreadsheet_name}}
        spreadsheet = service.spreadsheets().create(
            body=spreadsheet, fields='spreadsheetId').execute()
        return spreadsheet.get('spreadsheetId')

    def search_spreadsheet(self, spreadsheet_name: str):
        '''
        Searche for the spreadsheet in Google Drive and return the spreadsheet ID.
        
        Since it is using Google Drive API, the scope must include reading
        files in Google Drive.
        
        If you want customized query, use `GoogleDrive.search_file()` instead.
        
        Args:
          spreadsheet_name: String
            The name of the spreadsheet. There is no file extension.
        
        Return:
          Dictionary.
            Key: Spreadsheet name.
            Value: List of spreadsheet ID in case there are duplicate file names.
        '''
        result = self.search_file(file_name=spreadsheet_name)
        return result

    def get_spreadsheet_property(self, spreadsheet_id: str):
        '''
        Get spreadsheet property and sheet property.
        
        Spreadsheet property includes the title, locale, timeZone, defaultFormat, etc.
        
        Sheet property includes sheetID, sheetIndex, sheetRowCount, and sheetColCount.
        
        Official API guide:
        https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/get
        
        Args:
          spreadsheet_id: String
            Spreadsheet ID.
            
        Return:
          Tuple: (spreadsheet_property, sheet_property)
            spreadsheet_property: Dictionary
              The entire spreadsheet property. It is the superset of the sheet property.
              Structure of the response:
              https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets#Spreadsheet
            sheet_property: Dictionary
              sheetId: Dictionary, key: sheet name, value: sheet ID
                The unique ID of each sheet regardless of position.
              sheetIndex: Dictionary, key: sheet name, value: sheet index
                The position of the sheet starting from 0.
              sheetRowCount: Dictionary, key: sheet name, value: sheet row count
                The numbder of rows in sheet. Note that this is not the number of 
                rows that contains data.It is the boundary of the sheet.
              sheetColCount: Dictionary, key: sheet name, value: sheet column count
                The numbder of columns in sheet. Note that this is not the number 
                of columns that contains data.It is the boundary of the sheet.
        '''
        service = build('sheets', 'v4', credentials=self.creds)
        request = service.spreadsheets().get(spreadsheetId=spreadsheet_id,
                                             includeGridData=False)
        # Spreadsheet property
        spreadsheet_property = request.execute()

        # Sheet property
        sheetId = {
            d['properties']['title']: d['properties']['sheetId']
            for d in spreadsheet_property['sheets']
        }
        sheetIndex = {
            d['properties']['title']: d['properties']['index']
            for d in spreadsheet_property['sheets']
        }
        sheetRowCount = {
            d['properties']['title']:
            d['properties']['gridProperties']['rowCount']
            for d in spreadsheet_property['sheets']
        }
        sheetColCount = {
            d['properties']['title']:
            d['properties']['gridProperties']['columnCount']
            for d in spreadsheet_property['sheets']
        }
        sheet_property = {
            'sheetId': sheetId,
            'sheetIndex': sheetIndex,
            'sheetRowCount': sheetRowCount,
            'sheetColCount': sheetColCount
        }
        return spreadsheet_property, sheet_property

    def download_spreadsheet(self, spreadsheet_id: str, save_as=''):
        '''
        Download the spreadsheet by given the spreadsheet ID
        and return a file pointer or save it as a file.
        
        Supported file formats: .xlsx, .csv, .pdf.
        For unsupported file formats i.e. Open Office sheet,
        sheet only, and HTML, use `GoogleDrive.download_file()`.
        
        Official API guide:
        https://developers.google.com/drive/api/v3/manage-downloads#download_a_file_stored_on_google_drive
        
        Args:
          spreadsheet_id: String
            The spreadsheet ID.
          save_as: String, default ''
            '': Return a file pointer.
            'Excel': Save as '{Spreadsheet name}.xlsx'. Return None.
            'CSV': Save as '{Spreadsheet name}.csv'. Return None.
              First sheet only.
            'PDF': Save as '{Spreadsheet name}.pdf'. Return None.
            '*.xlsx': Save as '*.xlsx'. Return None.
            '*.csv': Save as '*.csv'. Return None.
            '*.pdf': Save as '*.pdf'. Return None.
        '''
        spreadsheet_name = self.get_file_metadata(file_id=spreadsheet_id,
                                                  fields='name')['name']
        mimeType = {
            'Excel':
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'Open Office sheet':
            'application/x-vnd.oasis.opendocument.spreadsheet',
            'PDF': 'application/pdf',
            'CSV': 'text/csv'
        }

        if save_as == '':
            result = self.download_file(file_id=spreadsheet_id,
                                        mimeType=mimeType['Excel'])
        elif save_as == 'Excel':
            result = self.download_file(
                file_id=spreadsheet_id,
                mimeType=mimeType['Excel'],
                save_as='{0}.xlsx'.format(spreadsheet_name))
        elif save_as == 'CSV':
            result = self.download_file(
                file_id=spreadsheet_id,
                mimeType=mimeType['CSV'],
                save_as='{0}.csv'.format(spreadsheet_name))
        elif save_as == 'PDF':
            result = self.download_file(
                file_id=spreadsheet_id,
                mimeType=mimeType['PDF'],
                save_as='{0}.pdf'.format(spreadsheet_name))
        elif save_as[-5:] == '.xlsx':
            result = self.download_file(file_id=spreadsheet_id,
                                        mimeType=mimeType['Excel'],
                                        save_as=save_as)
        elif save_as[-4:] == '.csv':
            result = self.download_file(file_id=spreadsheet_id,
                                        mimeType=mimeType['CSV'],
                                        save_as=save_as)
        elif save_as[-4:] == '.pdf':
            result = self.download_file(file_id=spreadsheet_id,
                                        mimeType=mimeType['PDF'],
                                        save_as=save_as)
        else:
            raise Exception(
                textwrap.dedent('''\
                {0} is not a supported file format.
                Please check the `GoogleSheet.download_spreadsheet()` docstring.
                Or you may want to use `GoogleDrive.download_file()` method.\
                '''.format(save_as)))
        return result

    def clear_sheet(self, spreadsheet_id: str, range_):
        '''
        Clears values from a spreadsheet
        
        Only values are cleared -- all other properties of 
        the cell (such as formatting, data validation, etc..) are kept.
        
        Official API guide:
        https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/clear
        
        Args:
          spreadsheet_id: String
        '''
        pass
    
    def update_value(self):
        '''
        Update the value on cell basis.
        
        Official API guide:
        https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/batchUpdate
        '''
        pass
    
    def update_column_format(self):
        '''
        Update the column format.
        
        Supported format: date, number, currency
        
        Officail API guide:
        https://developers.google.com/sheets/api/samples/formatting
        https://developers.google.com/sheets/api/guides/formats
        https://developers.google.com/sheets/api/guides/batchupdate
        '''
        pass