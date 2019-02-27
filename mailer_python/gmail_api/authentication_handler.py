import os
import pickle
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

class GmailAccountAuthenticationHandler:
    DEFAULT_CREDENTIALS_FILE=os.path.join(settings.BASE_DIR,'gmail_api/.credentials/client_secret.json')
    SCOPES=[]

    def __init__(self,scopes=[],credentials_path=""):
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





class GmailAccountAuthenticationHandlerv2:
    DEFAULT_CREDENTIALS_FILE=os.path.join(settings.BASE_DIR,'gmail_api/.credentials/client_secret.json')
    SCOPES=[]

    def __init__(self,scopes=[],credentials_path=""):
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