import abc
import os
import pickle
from google.oauth2 import service_account
from oauth2client import client
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from mailer import settings
from .config import GmailConfig


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
    SCOPES=[]
    def __init__(self,scopes=[]):
        if not os.path.exists(GmailConfig.SERVICE_ACCOUNT_SECRET):
            raise(FileNotFoundError("File {} not found".format(GmailConfig.SERVICE_ACCOUNT_SECRET)))
        if scopes:self.SCOPES=scopes

    def get_credentials(self):
        return service_account.Credentials.from_service_account_file(GmailConfig.SERVICE_ACCOUNT_SECRET, scopes=self.SCOPES)

class GmailAccountAuthenticationHandler(AbstractAccountAuthenticationHandler):
    SCOPES=[]

    def __init__(self,scopes=[],credentials_path=""):
        if not os.path.exists(GmailConfig.OAUTH2_ACCOUNT_SECRET):
            raise(FileNotFoundError("File {} not found".format(GmailConfig.OAUTH2_ACCOUNT_SECRET)))
        if scopes:self.SCOPES=scopes

    def get_credentials(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        token_file=GmailConfig.TOKEN_PICKLE_FILE
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    GmailConfig.OAUTH2_ACCOUNT_SECRET, self.SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        return creds