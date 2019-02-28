import abc
import os
import pickle
from google.oauth2 import service_account
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from mailer import settings

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

GMAIL_SCOPES={
    "gmail.all":"https://mail.google.com/",
    # Send messages only. No read or modify privileges on mailbox.
    "gmail.readonly":"https://www.googleapis.com/auth/gmail.readonly",
    # 	Read all resources and their metadata—no write operations.
    "gmail.compose":"https://www.googleapis.com/auth/gmail.compose",
    # Create, read, update, and delete drafts. Send messages and drafts.
    "gmail.insert":"https://www.googleapis.com/auth/gmail.insert",
    # Insert and import messages only.
    "gmail.labels":"https://www.googleapis.com/auth/gmail.labels",
    # Create, read, update, and delete labels only.
    "gmail.modify":"https://www.googleapis.com/auth/gmail.modify",
    # All read/write operations except immediate, permanent deletion of threads and messages, bypassing Trash.
    "gmail.metadata":"https://www.googleapis.com/auth/gmail.metadata",
    # Read resources metadata including labels, history records, and email message headers, but not the message body or attachments.
    "gmail.settings.basic":"https://www.googleapis.com/auth/gmail.settings.basic",
    # Manage basic mail settings.
    "gmail.settings.sharing":"https://www.googleapis.com/auth/gmail.settings.sharing",
    # Manage sensitive mail settings, including forwarding rules and aliases.
    "gmail.send":"https://www.googleapis.com/auth/gmail.send"
    # Send messages only. No read or modify privileges on mailbox.
}


class AbstractAccountAuthenticationHandler(abc.ABC):
    DEFAULT_CREDENTIALS_FILE=""
    SCOPES=[]
    @abc.abstractmethod
    def get_credentials(self):
        pass


class ServiceAccountAuthenticationHandler(AbstractAccountAuthenticationHandler):
    DEFAULT_CREDENTIALS_FILE=""
    SCOPES=[]
    def __init__(self,scopes=[],credentials_path=""):
        if not os.path.exists(os.path.basename(self.DEFAULT_CREDENTIALS_FILE)):
            os.mkdir(os.path.basename(self.DEFAULT_CREDENTIALS_FILE))
        if scopes:self.SCOPES=scopes
        if credentials_path:self.DEFAULT_CREDENTIALS_FILE=credentials_path

    def get_credentials(self):
        return service_account.Credentials.from_service_account_file(self.DEFAULT_CREDENTIALS_FILE, scopes=self.SCOPES)

class GmailAccountAuthenticationHandler(AbstractAccountAuthenticationHandler):
    DEFAULT_CREDENTIALS_FILE=os.path.join(settings.BASE_DIR,'gmail_api/.credentials/client_secret.json')
    SCOPES=[]

    def __init__(self,scopes=[],credentials_path=""):
        if not os.path.exists(os.path.basename(self.DEFAULT_CREDENTIALS_FILE)):
            os.mkdir(os.path.basename(self.DEFAULT_CREDENTIALS_FILE))
        if scopes:self.SCOPES=scopes
        if credentials_path:self.DEFAULT_CREDENTIALS_FILE=credentials_path

    def get_credentials(self):
        credential_file= os.path.join(settings.BASE_DIR,'gmail_api/.credentials/gmail-api-creds.json')
        store = Storage(credential_file) 
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(self.DEFAULT_CREDENTIALS_FILE, self.SCOPES)
            creds = tools.run_flow(flow, store)
            if flags:
                creds = tools.run_flow(flow, store, flags)
        return creds

class GmailAccountAuthenticationHandlerv2(AbstractAccountAuthenticationHandler):
    DEFAULT_CREDENTIALS_FILE=os.path.join(settings.BASE_DIR,'gmail_api/.credentials/client_secret.json')
    SCOPES=[]

    def __init__(self,scopes=[],credentials_path=""):
        if not os.path.exists(os.path.basename(self.DEFAULT_CREDENTIALS_FILE)):
            os.mkdir(os.path.basename(self.DEFAULT_CREDENTIALS_FILE))
        if scopes:self.SCOPES=scopes
        if credentials_path:self.DEFAULT_CREDENTIALS_FILE=credentials_path

    def get_credentials(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        token_file=os.path.join(settings.BASE_DIR,'gmail_api/.credentials/token.pickle')
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.DEFAULT_CREDENTIALS_FILE, self.SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        return creds