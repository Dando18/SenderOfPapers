import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

from credentials import *

class send_server:

    def __init__(self, host='127.0.0.1', port=587):
        '''
        Create a send_server.
        host: host name of server
        port: port number
        '''
        self.host = host
        self.port = port

        

    def __enter__(self):
        '''
        Create the smtp server for sending mail
        '''
        self.smtp_server = smtplib.SMTP(host=self.host, port=self.port)
        self.smtp_server.starttls()
        self.smtp_server.login(get_from_email(), get_password())
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.smtp_server.close()


    def send(self, fro, to, subject='default subject', text='default email text', files=None):
        '''
        Send an email across this server
        fro: who to send from
        to: who to send to
        subject: email subject
        text: text of email
        files: attachments
        '''
        if not isinstance(to, list):
            to = [to]

        msg = MIMEMultipart()
        msg['From'] = fro
        msg['To'] = ', '.join(to)   # allows multiple to addresses
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(text))

        for f in files or []:
            with open(f, 'rb') as attachment:
                ext = f.split('.')[-1:]
                part = MIMEApplication(attachment.read(), _subtype=ext)
                part.add_header('content-disposition', 'attachment', filename=basename(f))

            msg.attach(part)
    
        self.smtp_server.sendmail(fro, to, msg.as_string())
        
        