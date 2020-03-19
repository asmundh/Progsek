import re

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


def validate_password(password, attributes):
    with open("10-million-password-list-top-10000.txt") as doc:
        content = doc.read()
        if password in content:
            return False, "too common"

    for val in attributes:
        if val.lower() in password.lower() and len(val) > 3:
            return False, "Password cannot contain any input from the input fields"

    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    elif not re.search("[a-z]", password):
        return False, "Password must contain at least one lowercase character"
    elif not re.search("[A-Z]", password):
        return False, "Password must contain at least one uppercase character"
    elif not re.search("[0-9]", password):
        return False, "Password must contain include at least one number"
    elif not re.search("[_@$?]", password):
        return False, "Password must contain at least one of the characters: _@$?"
    elif re.search("\s", password):
        return False, "Password cannot contain whitespaces"

    return True, "Password is good"
