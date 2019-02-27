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


class AbstractGmailHandler(abc.ABCMeta):
    pass


class GmailHandler(AbstractGmailHandler):
    service=None

    def create_service(self,credentials):
        self.service=discovery.build("gmail","v1",credentials=credentials)
        return self.service

    def create_message(self,sender, to, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_bytes())}

    def create_message_with_attachment(self,
        sender, to, subject, message_text, file):
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


    def send_message(self,message,userId="me"):
        pass

    def list_labels(self,userId="me"):
        return self.service.users().labels().list(userId=userId).execute()



