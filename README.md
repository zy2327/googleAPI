# googleAPI

[![PyPI Latest Release](https://img.shields.io/pypi/v/googleAPI.svg)](https://pypi.org/project/googleAPI/)
[![License](https://img.shields.io/pypi/l/googleAPI.svg)](https://github.com/zy2327/googleAPI/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/googleapi)](https://pepy.tech/project/googleapi)
[![HitCount](http://hits.dwyl.com/zy2327/googleAPI.svg)](http://hits.dwyl.com/zy2327/googleAPI)
[![Python Versions](https://img.shields.io/pypi/pyversions/googleAPI.svg)](https://pypi.org/project/googleAPI/)
[![Read the Docs](https://readthedocs.org/projects/googleapi/badge/?version=latest)](https://googleapi.readthedocs.io/en/latest/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a python package that handles all the work with Google services, including Google Drive, Google Sheet, and Gmail. It is a high-level interface of the [Google API](https://developers.google.com/apis-explorer). The downside of using the official Google API directly is that its documentation is written in Python 2.x, making it hard to follow.

To use the google API, the first step is to get the 'credentials.json'. The most easiest way would be visiting the [Google Drive API Quickstart](https://developers.google.com/drive/api/v3/quickstart/go) and click the `Enable the Drive API` button in the "Step 1: Turn on the Drive API" section. Then voliá, there you go! No need to deal with the project, service account, etc.

This package utilize [Drive API v3](https://developers.google.com/drive/api/v3/reference), [Google Sheets API v4](https://developers.google.com/sheets/api/reference/rest), [Gmail API v1](https://developers.google.com/gmail/api/v1/reference/).


## Installation

`pip install googleAPI`

## Dependencies

- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib

## Documentation

Read the documentation at [https://googleapi.readthedocs.io/en/latest/](https://googleapi.readthedocs.io/en/latest/).

### Credential

Credential is needed for every API. Thus, `GoogleCredential()` is the base class of all the other classes.

_Note: Unless you want to write customized functions, you could skip this section._

Suppose we want to get Google Drive credential with all scopes to write customized functions.

``` python
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
```

The argument `credential_scopes` is required. For all the scopes you can choose, visit [OAuth 2.0 Scopes for Google APIs](https://developers.google.com/identity/protocols/oauth2/scopes).


### GoogleDrive

Google Drive is a cloud storage where you store the files and folder. `GoogleDrive()` enable you to search for file ID, get file metadata, download files, etc.

Suppose we want to download a .csv file from the Google Drive.

``` python
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
```

### GoogleSheet

Suppose we want to download a GoogleSheet named `Google Sheet 1` as an Microsoft Excel file `Google Sheet 1.xlsx`.

``` python
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
```

Suppose we already have the spreadsheet ID and we just want to get the values
from a particular sheet `Sheet1`.
``` python
values = gs.get_values(spreadsheet_id, range_="'Sheet1'")
```



