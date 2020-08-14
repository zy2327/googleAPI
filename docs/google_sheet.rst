GoogleSheet
===========

``GoogleSheet()`` is a child class of ``GoogleDrive()``. 
It enables you to read a specific range of cells, download the spreadsheet,
and upload the values in the spreadsheet.

Terminology
-----------
  
**Spreadsheet**: The whole file. Same level as an Microsoft Excel file.

Every API method requires a ``spreadsheetId`` parameter which is used 
to identify which spreadsheet is to be accessed or altered.

The spreadsheet ID is a string containing letters, numbers, 
and some special characters. The following regular expression can be 
used to extract the spreadsheet ID from a Google Sheets URL:

.. code-block:: python

    /spreadsheets/d/([a-zA-Z0-9-_]+)

**Sheet**: A tab inside the spreadsheet. Same as Excel sheet.

**A1 Notation**: 

Some API methods require a range in A1 notation. 
This is a string like ``Sheet1!A1:B2``, that refers to a group of cells 
in the spreadsheet, and is typically used in formulas. 
For example, valid ranges are:

- ``Sheet1!A1:B2`` refers to the first two cells in the top two rows of Sheet1.
- ``Sheet1!A:A`` refers to all the cells in the first column of Sheet1.
- ``Sheet1!1:2`` refers to the all the cells in the first two rows of Sheet1.
- ``Sheet1!A5:A`` refers to all the cells of the first column of Sheet 1, from row 5 onward.
- ``A1:B2`` refers to the first two cells in the top two rows of the first visible sheet.
- ``Sheet1`` refers to all the cells in Sheet1.

Named ranges are also supported. When a named range conflicts with a sheet's name, the named range is preferred.

If the sheet name has spaces or starts with a bracket, surround the sheet name with single quotes (``'``), 
e.g ``'Sheet One'!A1:B2``. 
For simplicity, it is safe to always surround the sheet name with single quotes.

|

For more information, refer to the |Google Sheet concept|.


GoogleSheet.\_\_init\_\_
-------------------------

**\_\_init\_\_(
self,
creds=None,
credential_path="",
credential_scopes=["https://www.googleapis.com/auth/drive"],
token_prefix="GoogleDrive\_",
token_suffix=""
)**

Initialize the credential.
    
If credential ``creds`` is provided, this method will use it directly 
if it is valid.
        
Otherwise, it will use ``credential_path`` and ``credential_scopes`` to
get the token.
        
**Args:**

  **creds:** *None or google.oauth2.credentials.Credentials, default None*
  
  **credential_path:** *String, default ''*

    Path to the credential with either 'token.pickle' or
    'credentials.json' in it.

  **credential_scopes:** *List of strings, default ['https://www.googleapis.com/auth/drive']*
    
    Scope of the credential. Default scope can
    'See, edit, create, and delete all of your Google Drive files'.
    Details:
    https://developers.google.com/identity/protocols/oauth2/scopes#sheets
          
  **token_prefix:** *String, default 'GoogleDrive\_'*

    Prefix of token file. eg. '{token_prefix}token.pickle'.

  **token_suffix:** *String, default ''*

    Suffix of token file. eg. 'token{token_suffix}.pickle'.


GoogleSheet.create_spreadsheet
------------------------------

**create_spreadsheet(self, spreadsheet_name)**

Creates a spreadsheet, returning the newly created spreadsheet's ID.
        
Official API guide:
https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/create
        
**Args:**

  **spreadsheet_name:** *String*

    The name of the spreadsheet.
    
**Return:**

    **spreadsheet ID**: String


GoogleSheet.search_spreadsheet
------------------------------

**search_spreadsheet(self, spreadsheet_name)**

Searche for the spreadsheet in Google Drive and return the spreadsheet ID.

Since it is using Google Drive API, the scope must include reading
files in Google Drive.

If you want customized query, use ``GoogleDrive.search_file()`` instead.

**Args:**

  **spreadsheet_name:** *String*
    
    The name of the spreadsheet. There is no file extension.

**Return:**

  **Dictionary**

  - Key: Spreadsheet name.
  - Value: List of spreadsheet ID in case there are duplicate file names.


GoogleSheet.get_spreadsheet_property
------------------------------------

**get_spreadsheet_property(self, spreadsheet_id)**

Get spreadsheet property and sheet property.

Spreadsheet property includes the title, locale, timeZone, defaultFormat, etc.

Sheet property includes sheetID, sheetIndex, sheetRowCount, and sheetColCount.

Official API guide:
https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/get

**Args:**

  **spreadsheet_id:** *String*

    Spreadsheet ID.
    
**Return:**

  **Tuple: (spreadsheet_property, sheet_property)**

    - **spreadsheet_property:** *Dictionary*

      The entire spreadsheet property. It is the superset of the sheet property.

      Structure of the response:
      https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets#Spreadsheet

    - **sheet_property:** *Dictionary*
      
      - sheetId: Dictionary, key: sheet name, value: sheet ID

        The unique ID of each sheet regardless of position.
    
      - sheetIndex: Dictionary, key: sheet name, value: sheet index

        The position of the sheet starting from 0.

      - sheetRowCount: Dictionary, key: sheet name, value: sheet row count

        The numbder of rows in sheet. Note that this is not the number of 
        rows that contains data.It is the boundary of the sheet.

      - sheetColCount: Dictionary, key: sheet name, value: sheet column count

        The numbder of columns in sheet. Note that this is not the number 
        of columns that contains data.It is the boundary of the sheet.


GoogleSheet.download_spreadsheet
--------------------------------

**download_spreadsheet(self, spreadsheet_id: str, save_as="")**

Download the spreadsheet by given the spreadsheet ID
and return a file pointer or save it as a file.

Supported file formats: .xlsx, .csv, .pdf.
For unsupported file formats i.e. Open Office sheet,
sheet only, and HTML, use ``GoogleDrive.download_file()``.

Official API guide:
https://developers.google.com/drive/api/v3/manage-downloads#download_a_file_stored_on_google_drive

**Args:**

  **spreadsheet_id:** *String*

    The spreadsheet ID.

  **save_as:** *String, default \'\'*

    - \'\': Return a file pointer.
    - 'Excel': Save as '{Spreadsheet name}.xlsx'. Return None.
    - 'CSV': Save as '{Spreadsheet name}.csv'. Return None.
      First sheet only.

    - 'PDF': Save as '{Spreadsheet name}.pdf'. Return None.
    - '*.xlsx': Save as '*.xlsx'. Return None.
    - '*.csv': Save as '*.csv'. Return None.
    - '*.pdf': Save as '*.pdf'. Return None.

**Return:**

  **None** or **file pointer** depending on the ``save_as``.


GoogleSheet.get_values
----------------------

**def get_values(
self,
spreadsheet_id,
range\_,
value_render_option=None,
date_time_render_option=None,
):**

Get a single value, a range of values, and several ranges of values.

Use ``GoogleSheet.download_spreadsheet()`` if you want to get the
entire spreadsheet.

Official API guide:

For single range:
https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get

For multiple ranges:
https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/batchGet

**Example:**

  Get the entire sheet of `Sheet 1`.

  .. code-block:: python

      >>> gs.get_values(spreadsheet_id, "'Sheet 1'")

  Get the value of cell `A5` in `Sheet 1`.

  .. code-block:: python

      >>> gs.get_values(spreadsheet_id, "'Sheet 1'!A5")

**Args:**

  **spreadsheet_id:** *String*

  **range\_:** *String or List of strings in A1 notation*
    
    - String: A single sheet, A single range
    - List of strings: Several ranges
    - value_render_option: String, default None

      How values should be represented in the output.
      The default render option is ``ValueRenderOption.FORMATTED_VALUE``.
      Details:
      https://developers.google.com/sheets/api/reference/rest/v4/ValueRenderOption

    - date_time_render_option: String, default None
      How dates, times, and durations should be represented in the output.
      Details:
      https://developers.google.com/sheets/api/reference/rest/v4/ValueRenderOption

**Return:**

    **ValueRange** in Dictionary

    Details:
    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values#resource:-valuerange


GoogleSheet.clear_values
------------------------

**clear_values(self, spreadsheet_id: str, range_)**

Clear values from a spreadsheet.

Only values are cleared -- all other properties of 
the cell (such as formatting, data validation, etc..) are kept.

Official API guide:
https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/clear

**Args:**
    **spreadsheet_id:** String
    **range\_:** String, A1 notation

**Return:**
    **Dictionary, cleared range**

    .. code-block:: python

        {
        "spreadsheetId": string,
        "clearedRange": string
        }


GoogleSheet.update_values
-------------------------

**update_values(self, spreadsheet_id, data, value_input_option="RAW")**

Sets values in a range of a spreadsheet.

Official API guide:
https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update

**Args:**

  **spreadsheet_id:** *String*

  **data:** *ValueRange in Dictionary*

    .. code-block:: python

        {
            "range": string,
            "majorDimension": enum (Dimension),
            "values": [
            array
            ]
        }

    Details:
    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values#ValueRange
    
**Return:**

    **Dictionary in structure:**
    
    .. code-block:: python

        {
        "spreadsheetId": string,
        "totalUpdatedRows": integer,
        "totalUpdatedColumns": integer,
        "totalUpdatedCells": integer,
        "totalUpdatedSheets": integer,
        "responses": [
            {
            object (UpdateValuesResponse)
            }
        ]
        }




.. |Google Sheet concept| raw:: html

   <a href="https://developers.google.com/sheets/api/guides/concepts" target="_blank">Google Sheet concept</a>

