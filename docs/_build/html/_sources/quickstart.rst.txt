Quick Start
===========

This is a python package that handles all the work with Google services, 
including Google Drive, Google Sheet, and Gmail. 
It is a high-level interface of the |Google API|. 
The downside of using the official Google API directly is that its documentation is written in Python 2.x, 
making it hard to follow.

To use the google API, the first step is to get the 'credentials.json'. 
The most easiest way would be visiting the |Google Drive API Quickstart| 
and click the ``Enable the Drive API`` button in the "Step 1: Turn on the Drive API" section. 
Then voliá, there you go! No need to deal with the project, service account, etc.

This package utilize |Drive API v3|, |Google Sheets API v4|, |Gmail API v1|.


Installation
------------

``pip install googleAPI``

Dependencies
------------

- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib

Documentation
-------------

Credential
^^^^^^^^^^

Credential is needed for every API. Thus, ``GoogleCredential()`` is the base class of all the other classes.

*Note: Unless you want to write customized functions, you could skip this section.*

Suppose we want to get Google Drive credential with all scopes to write customized functions.

.. code-block:: python

    # Step 1: import the module
    from googleAPI.credential import *

    # Step 2: Instance `GoogleCredential()` class
    gc = GoogleCredential()

    # Step 3: Get credential
    # `credential_path` is the place where 'credentials.json' is stored.
    # There will be a prompt web page that will download the 'token.pickle'
    # into `credential_path`.
    creds = gc.credential(credential_path='',
                        credential_scopes=['https://www.googleapis.com/auth/drive'])


The argument ``credential_scopes`` is required. For all the scopes you can choose, 
visit |OAuth 2.0 Scopes for Google APIs|.


GoogleDrive
^^^^^^^^^^^

Google Drive is a cloud storage where you store the files and folder. ``GoogleDrive()`` enable you to search for file ID, get file metadata, download files, etc.

Suppose we want to download a .csv file from the Google Drive.

.. code-block:: python

    # Step 1: import the module
    from googleAPI.drive import *

    # Step 2: Instance `GoogleDrive` class with credential
    # If this is the first time you use this package, `credential_path` is 
    # the place where 'credentials.json' is stored. There will be a prompt
    # web page that will download the 'GoogleDrive_token.pickle' into `credential_path`.
    # If you already have 'GoogleDrive_token.pickle' file, `credential_path` 
    # is the place where it is stored.
    # If you already have the credential in the run time, use `creds` argument.
    gd = GoogleDrive(credential_path='')

    # Step 3: Search the file ID in Google Drive
    # Use the file name to locate the file ID. File ID is the unique identifier
    # that Google API uses.
    # You can also find the file ID inside the link if you open the file in a
    # web page. The ID is the characters after `/d/{ID}`.
    file_id = gd.search_file('test.csv')

    # Step 4: Download the file
    # If you want to download the file into run time as a file pointer, leave the
    # `save_as` argument blank.
    # If you want to download it as a file, specify the `save_as` argument.
    gd.download_file(file_id['test.csv'][0], save_as='test.csv')


GoogleSheet
^^^^^^^^^^^

Suppose we want to download a GoogleSheet named 'Google Sheet 1' as an Microsoft Excel file 'Google Sheet 1.xlsx'.

.. code-block:: python

    # Step 1: import the module
    from googleAPI.sheet import *

    # Step 2: Instance `GoogleSheet` class with credential
    gs = GoogleSheet(credential_path='')

    # Step 3: Find the Google Sheet ID using spreadsheet name
    # The result of the `GoogleSheet.search_spreadsheet()` is
    # saved in a list inside a dictionary in line with the
    # `GoogleDrive.search_files()`
    spreadsheet_id = gs.search_spreadsheet("Google Sheet 1")[
                "Google Sheet 1"
            ][0]

    # Step 4: Download the Google Sheet
    gs.download_spreadsheet(spreadsheet_id, 
                            save_as="Google Sheet 1.xlsx")


Suppose we already have the spreadsheet ID and we just want to get the values
from a particular sheet `Sheet1`.

.. code-block:: python

    values = gs.get_values(spreadsheet_id, range_="'Sheet1'")



.. |Google API| raw:: html
  
  <a href="https://developers.google.com/apis-explorer" target="_blank">Google API</a>

.. |Google Drive API Quickstart| raw:: html

  <a href="https://developers.google.com/drive/api/v3/quickstart/go" target="_blank">Google Drive API Quickstart</a>

.. |Drive API v3| raw:: html

  <a href="https://developers.google.com/drive/api/v3/reference" target="_blank">Drive API v3</a>

.. |Google Sheets API v4| raw:: html

  <a href="https://developers.google.com/sheets/api/reference/rest" target="_blank">Google Sheets API v4</a>

.. |Gmail API v1| raw:: html

  <a href="https://developers.google.com/gmail/api/v1/reference/" target="_blank">Gmail API v1</a>

.. |OAuth 2.0 Scopes for Google APIs| raw:: html

  <a href="https://developers.google.com/identity/protocols/oauth2/scopes" target="_blank">OAuth 2.0 Scopes for Google APIs</a>