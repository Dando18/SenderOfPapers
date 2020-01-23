

def get_credentials(file_name='credentials'):
    '''
    Not a great way to deal with credentials. Needs a file like...

    '
    TO send_to_email_addr@gmail.com
    FROM email_set_up_to_send@gmail.com
    PASS password for from email
    '

    Returns:
    tuple -- to email, from email, password for from email
    '''
    keys = {}
    with open(file_name, 'r') as f:
        for line in f.readlines():
            if line == '':
                continue
            vals = line.split(' ')
            keys[vals[0]] = vals[1]
    
    return keys['TO'], keys['FROM'], keys['PASS']


def get_to_email(file_name='credentials'):
    return get_credentials(file_name)[0]

def get_from_email(file_name='credentials'):
    return get_credentials(file_name)[1]

def get_password(file_name='credentials'):
    return get_credentials(file_name)[2]