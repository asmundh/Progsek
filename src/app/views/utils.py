import hashlib, binascii, os

def get_nav_bar(session):
    """
    Generates the page nav bar

        :return: The navigation bar HTML markup
    """
    result = '<nav>'
    result += ' <ul>'
    result += '    <li><h1 id="title">Beelance2</h1></li>'
    result += '    <li><a href="/">Home</a></li>'
    if session.username:
        result += '    <li><a href="logout">Logout</a></li>'
        result += '    <li><a href="new_project">New</a></li>'
    else:
        result += '    <li><a href="register">Register</a></li>'
        result += '    <li><a href="login">Login</a></li>'
    result += '    <li><a href="open_projects">Projects</a></li>'
    result += ' </ul>'
    result += '</nav>'
    return result

                        
def get_element_count(data, element):
    """
    Determine the number of tasks created by removing 
    the four other elements from count and divide by the 
    number of variables in one task.
     
        :param data: The data object from web.input
        :return: The number of tasks opened by the client
    """
    task_count = 0
    while True:
        try:
            data[element+str(task_count)]
            task_count += 1
        except:
            break
    return task_count

def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')

    return pwdhash == stored_password

