import sys
from apiclient.http import BatchHttpRequest

from mailer import settings
from gmail_api import GmailHandler,GmailAccountAuthenticationHandler,GMAIL_SCOPES,ServiceAccountAuthenticationHandler

from parsers import csv_parsers

gmail_authentication_handlers={
    "service_account":ServiceAccountAuthenticationHandler,
    "oauth2":GmailAccountAuthenticationHandler,
}

def validate_args(r):
    if r.csv_parser not in csv_parsers.keys():
        sys.exit("Invalid csv parser\nValid Parsers:{}".format(list(csv_parsers.keys())))
    if r.auth not in gmail_authentication_handlers.keys():
        sys.exit("Invalid Authentication Handler\nValid authentication Handlers:{}".format(list(gmail_authentication_handlers.keys())))
    return True


def main(user_input):
    # credentials scopes
    scopes=[
        GMAIL_SCOPES["gmail.all"],
    ]
    credentials=gmail_authentication_handlers[user_input.auth](scopes=scopes).get_credentials()

    # gmail handler
    gmail_handler=GmailHandler()
    if user_input.auth=="service_account":
        gmail_handler.create_service(credentials,delegated_email=user_input.sender)
    else:
        gmail_handler.create_service(credentials)

    #batch requests instance
    batch=BatchHttpRequest()

    # batch requests callback
    def batch_callback(request_id, response, exception):
        # @todo check if exception occured
        print(request_id, response, exception)

    #get message list from csvs
    csv_data=csv_parsers[user_input.csv_parser]().parse_csv_file(user_input.sender)

    for data in csv_data:
        message= gmail_handler.create_message(**data)
        batch.add(
            gmail_handler.send_message(message,batch=True,userId="me" if user_input.auth=="oauth2" else user_input.sender),
            callback=batch_callback,
        )
    batch.execute()


if __name__=="__main__":
    '''
    parser, sender,authentication
    '''
    import argparse
    parser = argparse.ArgumentParser(description='Send Emails from CSV file using Gmail API and a csv parser')
    parser.add_argument('-csv_parser', action='store',
                    dest='csv_parser',type=str,
                    help='Specify Csv parser to use')
    
    parser.add_argument('-sender', action='store',
                    dest='sender',type=str,
                    help='Senders Email')

    parser.add_argument('-auth', action='store',
                    dest='auth',type=str,
                    help='Authentication Type: oauth2, service_account')
    
    user_input=parser.parse_args()
    print(user_input.sender)
    validate_args(user_input)
    main(user_input)
    
