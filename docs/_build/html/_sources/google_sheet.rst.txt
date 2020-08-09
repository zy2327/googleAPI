GoogleSheet
===========

Terminology
-----------
  
**Spreadsheet**: The whole file. Same level as an Microsoft Excel file.

Every API method requires a ``spreadsheetId`` parameter which is used to identify which spreadsheet is to be accessed or altered.

The spreadsheet ID is a string containing letters, numbers, and some special characters. The following regular expression can be used to extract the spreadsheet ID from a Google Sheets URL:

.. code-block:: python
  
  /spreadsheets/d/([a-zA-Z0-9-_]+)

    
For more information, refer to the `Google Sheet concept<https://developers.google.com/sheets/api/guides/concepts>`. 