from mailer import settings
import os

class GmailConfig:
    SERVICE_ACCOUNT_SECRET=os.path.join(settings.BASE_DIR,'gmail_api/.credentials/service_account_secrets.json')
    OAUTH2_ACCOUNT_SECRET=os.path.join(settings.BASE_DIR,'gmail_api/.credentials/client_secret.json')
    TOKEN_PICKLE_FILE=os.path.join(settings.BASE_DIR,'gmail_api/.credentials/token.pickle')