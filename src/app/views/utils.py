
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
