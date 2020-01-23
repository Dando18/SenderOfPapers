'''
author: Daniel Nichols
brief: Run this with --check to check for new replies and --send to send the next mail.
        Nothing in here is robust and the entire project is somewhat GMAIL dependent.
'''
import sys
import os
from pathlib import Path
from send_server import send_server
from receive_server import receive_server
from credentials import *


def get_file_to_send(directory='./reading_list'):
    '''
    Get the next PDF to send. Just grabs the first PDF from directory alphabetically.
    The sender uses this function to pick next file. Use this to change how PDFs are chosen.

    Returns:
    a tuple (file_name, file_path)
    '''
    files = []
    with os.scandir(directory) as it:
        for f in it:
            if f.name.endswith('.pdf') and f.is_file():
                files.append((str(f.name), str(f.path)))
    files.sort(key=lambda x: x[0])
    return files[0]


def preprocess_files(directory='./reading_list'):
    '''
    Preprocess the files in the current directory.

    Removes spaces in pdf name.
    '''
    with os.scandir(directory) as it:
        for f in it:
            if ' ' in f.name and f.name.endswith('.pdf') and f.is_file():
                os.rename(directory + '/' + f.name, directory + '/' + f.name.replace(' ', '_'))


def receive():
    '''
    Uses the receive server (in receive_server.py) to check for responses in Inbox.
    If there are any, then the notes and PDF are moved to a folder in the notes directory.
    '''
    with receive_server('imap.gmail.com', port=587) as rs:
        for article_name, note_body in rs.get_all_notes():
            article_file = Path('./reading_list/' + str(article_name) + '.pdf')
            if not article_file.is_file():
                print('Error: Bad File Name. "' + str(article_name) + '" Not Found.')
                continue

            # check if notes folder exists -- make it if not
            notes_dir = Path('./notes')
            if not notes_dir.exists() or not notes_dir.is_dir():
                os.mkdir('./notes', 0o744)
            
            # create the article directory if necessary
            article_dir = Path('./notes/'+str(article_name))
            if not article_dir.exists() or not article_dir.is_dir():
                os.mkdir('./notes/'+str(article_name), 0o744)

            # move file
            os.rename('./reading_list/'+str(article_name)+'.pdf', \
                './notes/'+str(article_name)+'/'+str(article_name)+'.pdf')

            # write notes to file
            with open('./notes/'+str(article_name)+'/notes.txt', 'a') as f:
                f.write(note_body)
                
            

def send():
    '''
    Sends the next bit of mail. Uses get_file_to_send() to determine which file (pdf) 
    should be sent.
    '''
    with send_server('smtp.gmail.com', port=587) as ss:
        file_name, file_path = get_file_to_send()

        pretty_file_name = file_name
        if pretty_file_name.endswith('.pdf'):
            pretty_file_name = file_name[:-4]

        mail_text = 'Mail of today is: "' + str(pretty_file_name) + '".\n'

        ss.send(fro=get_from_email(), \
            to=get_to_email(), \
            subject='paper: "' + str(pretty_file_name) + '"', \
            text=mail_text, \
            files=[file_path])
        
    print('mail sent')



def main(argc, argv):

    # some stuff (i.e. os.scandir) is only python >3 
    if sys.version_info[0] < 3:
        raise Exception('Must be using Python 3')

    preprocess_files()

    # check for new papers
    if argv.count('--check') >= 1:
        receive()

    # send out the next paper
    if argv.count('--send') >= 1:
        send()
        


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
