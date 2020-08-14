GoogleCredential
================

``GoogleCredential()`` is the base class of all the other classes. It provides an access to the Google API credentials -- no matter if you have ever generated a ``token`` before.

GoogleCredential.credential
-----------------------------

**credential(credential_path="", credential_scopes=None, token_prefix="", token_suffix="")**

Initialize the Google credential.

If there is 'token.pickle' file in the ``credential_path`` and 
the token is valid, then it would load the pickle file.

*Note: Whenever you modify the credential scope, you have to delete 
the 'token.pickle' file and generate a new token.*

Otherwise, it would use 'credentials.json' file in the 
``credential_path``, prompt an authetication web page, request the 
user to confirm the ``credential_scopes``, and download the token
in the same folder.

You can customize the name of 'token.pickle' with ``token_prefix`` and 
``token_suffix`` in case there are tokens with different scopes.
        
For example, use 'GoogleDrive_token_all.pickle' to indicate this token
has all the scopes in Google Drive.
        
**Args:**

  **credential_path:** *String, default ''*

    Path of the credential files.

  **credential_scopes:** *None or String or List of strings, default None*

    Scope of the credential.

    - None: Would raise error.

    - String: A single scope.

    - List of strings: A list of scopes.
      Details: https://developers.google.com/identity/protocols/oauth2/scopes

  **token_prefix:** *String, default ''*

      Prefix of token file. eg. '{token_prefix}token.pickle'.

  **token_suffix:** *String, default ''*

      Suffix of token file. eg. 'token{token_suffix}.pickle'.
            
**Return:**

  **google.oauth2.credentials.Credentials**

GoogleCredential.credential_validation
--------------------------------------

**credential_validation(creds)**

Validate the token.

Check token is valid and not expired.
        
**Args:**
  **creds:** *google.oauth2.credentials.Credentials*
  
    Token waited to be validated.
        
**Return:**

  **Boolean.**
    
    True: Token is valid.
    
    False: Token is not valid.





.. |Google Drive API Quickstart| raw:: html

   <a href="https://developers.google.com/drive/api/v3/quickstart/go" target="_blank">Google Drive API Quickstart</a>

