
from apiclient.http import BatchHttpRequest

from mailer import settings
from gmail_api import GmailHandler,GmailAccountAuthenticationHandlerv2,GMAIL_SCOPES

from parsers import SimpleCsvEmailParser

# credentials scopes
scopes=[
    GMAIL_SCOPES["gmail.readonly"],
    GMAIL_SCOPES["gmail.send"]
]

credentials=GmailAccountAuthenticationHandlerv2(scopes=scopes).get_credentials()

# gmail handler
gmail_handler=GmailHandler()
gmail_handler.create_service(credentials)

#batch requests instance
batch=BatchHttpRequest()

# batch requests callback
def batch_callback(request_id, response, exception):
    # @todo check if exception occured
    print(request_id, response, exception)

#get message list from csvs
csv_data=SimpleCsvEmailParser().parse_csv_file("jackogina60@gmail.com","Results")

for data in csv_data:
    message= gmail_handler.create_message(**data)
    batch.add(
        gmail_handler.send_message(message,batch=True),
        callback=batch_callback,
    )
batch.execute()
