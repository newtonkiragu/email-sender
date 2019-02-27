import os
from mailer import settings

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
        return creds