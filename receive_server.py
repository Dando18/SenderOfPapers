import imaplib
import email
from credentials import *

class receive_server:


    def __init__(self, host='127.0.0.1', port='587'):
        '''
        Initializes a receive_server object at host 'host' and port 'port'.
        '''
        self.host = host
        self.port = port

    
    def __enter__(self):
        '''
        On entering a with block, the server will attempt to login.
        '''
        self.imap_server = imaplib.IMAP4_SSL(self.host)
        self.imap_server.login(get_from_email(), get_password())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''
        Safe exit at the end of the with block.
        '''
        self.imap_server.close()
        self.imap_server.logout()


    def get_all_notes(self):
        '''
        Gets the paper name and associated note in reply

        Returns:
        an iterator returning tuples containing the (paper name, notes)
        '''
        self.imap_server.select('Inbox')

        result, data = self.imap_server.search(None, 'UNSEEN')

        if result != 'OK':
            print('Error: Searching for UNSEEN failed.')
            return

        for index in data[0].split():
            result, data = self.imap_server.fetch(index, '(RFC822)')

            # mark msg as seen so we don't process it again
            self.imap_server.store(index, '+FLAGS', '\Seen')

            if result != 'OK':
                print('Error: Fetching message ' + str(index) + ' failed.')
                continue

            msg = email.message_from_bytes(data[0][1])

            hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
            subject = str(hdr)
            
            body = ''
            if msg.is_multipart():
                # walk thru parts of MIME message protocal
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get('Content-Disposition'))

                    if content_type == 'text/plain' and 'attachment' not in content_disposition:
                        body = part.get_payload(decode=True)
                        break
            else:
                body = msg.get_payload(decode=True)

            # change from b'' binary string to utf-8 normal string
            body = body.decode('utf-8')

            # remove lines starting with '>' (constructively...)
            lines = [l for l in body.split('\r\n') if not l.startswith('>')]
            
            # This is pretty screwy, but remove lines the lines with 'On .... write:'
            # at the end of the message. These are part of gmail's REPLY template
            for i in range(len(lines)-1, 0, -1):
                if lines[i].startswith('On '):
                    del lines[i]
                    break
                elif lines[i].endswith('wrote:'):
                    del lines[i]

            # join the lines back together 
            lines = '\r\n'.join(lines)
            
            # pull the quoted article title out
            article_name = ''
            start_idx = subject.find('\"')
            if start_idx != -1:
                end_idx = subject.find('\"', start_idx + 1)
                if end_idx != -1:
                    article_name = subject[start_idx+1:end_idx]

            yield article_name, lines
        