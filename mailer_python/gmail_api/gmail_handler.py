import abc
import base64
import os

from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import mimetypes

from apiclient import discovery


class AbstractGmailHandler(abc.ABC):
    pass


class GmailHandler(AbstractGmailHandler):
    '''
    Gmail api 
        reference: https://developers.google.com/gmail/api/v1/reference
        to impelement more methods
    '''
    service=None

    def create_service(self,credentials,service=None):
        '''
        Creates a service instance
        args:
            credentials instance
        Returns:
            gmail service instance
        '''
        if not service:
            service=discovery.build("gmail","v1",credentials=credentials)
        self.service=service
        return self.service

    def create_message(self,sender="", to="", subject="", message_text=""):
        '''
        Create a message for an email.
        Args:
            sender: Email address of the sender.
            to: Email address of the receiver.
            subject: The subject of the email message.
            message_text: The text of the email message.

        Returns:
            An object containing a base64url encoded email object.
        '''
        
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    def create_message_with_attachment(self,
    sender, to, subject, message_text, file):
        """Create a message for an email.

        Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
        file: The path to the file to be attached.

        Returns:
        An object containing a base64url encoded email object.
        """
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        msg = MIMEText(message_text)
        message.attach(msg)

        content_type, encoding = mimetypes.guess_type(file)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(file, 'rb')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(file, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(file, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(file, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
        filename = os.path.basename(file)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


    def send_message(self, message,userId="me",batch=False):
        """
        https://developers.google.com/gmail/api/v1/reference/users/messages/send
        Send an email message.

        Args:
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            message: Message to be sent.

        Returns:
            Sent Message.
        """
        try:
            if not batch:
                return (self.service.users().messages().send(userId=userId, body=message)
                        .execute())
            else:
                return self.service.users().messages().send(userId=userId, body=message)
        except Exception as e:
            print("Error: {}".format(e))
            return False

    def list_messages(self,userId="me",maxResults=100,labelIds=[],q=""):
        '''
        list user messages
        args(optional):
            userId
            maxResults
            labelIds

        Returns:
            retrieved list of messages
        '''
        try:
            return self.service.users().messages().list(userId=userId,maxResults=maxResults).execute()
        except Exception as e:
            print("Error: {}".format(e))
            return False

    def get_message(self,id,userId="me"):
        '''
        get specified message

        args:
            id: message id
            userId: user email
        Returns
            message object
        '''
        try:
            return self.service.users().messages().get(id=id,userId=userId).execute()
        except Exception as e:
            print("Error: {}".format(e))
            return False