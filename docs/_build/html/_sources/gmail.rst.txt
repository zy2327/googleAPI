Gmail
=======

``Gmail()`` is a child class of ``GoogleCredential()``. 
It lets you to send email, create draft, and upload attachments.

Gmail.\_\_init\_\_
-------------------------

**\_\_init\_\_(
self,
creds=None,
credential_path="",
credential_scopes=["https://mail.google.com/"],
token_prefix="Gmail\_",
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

  **credential_scopes:** *List of strings, default ['https://mail.google.com/']*
    
    Scope of the credential. Default scope can
    'See, edit, create, and delete all of your Google Drive files'.
    Details:
    https://developers.google.com/identity/protocols/oauth2/scopes#gmail
          
  **token_prefix:** *String, default 'Gmail\_'*

    Prefix of token file. eg. '{token_prefix}token.pickle'.

  **token_suffix:** *String, default ''*

    Suffix of token file. eg. 'token{token_suffix}.pickle'.


Gmail.create_message
--------------------

**create_message(sender, to, subject, message_text)**

Create a message for an email.

**Args:**

  **sender:** *String*

    Email address of the sender.

  **to:** *String or List*

    Email address of the receiver.

  **subject:** *String*

    The subject of the email message.

  **message_text:** *String*

    The text of the email message.

**Returns:**

  An object containing a base64url encoded email object.

Gmail.create_message_with_attachment
------------------------------------

**@staticmethod**

**create_message_with_attachment(sender, to, subject, message_text, files)**
        
Create a message for an email with attachment(s).

**Args:**

  **sender:** *String*

    Email address of the sender.
  
  **to:** *String or List*

    Email address(es) of the receiver.

  **subject:** *String*

    The subject of the email message.

  **message_text:** *String*

    The text of the email message.

  **files:** *String or List or Dictionary*

    The name of file(s) to be attached.

    - String: The name of a single file.

      Use it only when there is one file and
      the file is located at the default path.

    - List: Names of files.

      Use it only when the file is located at
      the default path.

    - Dictionary:

      - key: String, path of the files
      - value: List, files within the key

      eg. 
      
      .. code-block:: python

        {'/home/': ['file1','file2'], '/home/user/': ['file3']}

**Returns:**

  An object containing a base64url encoded email object.


Gmail.send_email
----------------

**send_email(self, sender, to, subject, message_text, files=None)**

Send email with/without attachment.

If `files` is None, it will generate the message
using `Gmail.create_message()`.

Otherwise, it will generate the message using
`Gmail.create_message_with_attachment()`.

Official API guide:
https://developers.google.com/gmail/api/guides/sending

**Args:**
  
  **sender:** *String*

    Email address of the sender.
    
  **to:** *String or List*

    Email address(es) of the receiver.
    
  **subject:** *String*

    The subject of the email message.
    
  **message_text:** *String*

    The text of the email message.

  **files:** *None or String or List or Dictionary, default None*

    The name of file(s) to be attached.

    - None: Send email without attachment.
    - String: The name of a single file.

      Use it only when there is one file and
      the file is located at the default path.

    - List: Names of files.
      Use it only when the file is located at
      the default path.
    
    - Dictionary:

      - key: String, path of the files
      - value: List, files within the key

      eg. 
      
      .. code-block:: python

        {'/home/': ['file1','file2'], '/home/user/': ['file3']}
    
**Return:**

    **Sent Message**

