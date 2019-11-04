
def get_nav_bar(session):
    result = '<nav>'
    result += ' <ul>'
    result += '    <li><h1 id="title">Beelance2</h1></li>'
    result += '    <li><a href="/">Home</a></li>'
    if session.username:
        result += '    <li><a href="logout">Logout</a></li>'
    else:
        result += '    <li><a href="register">Register</a></li>'
        result += '    <li><a href="login">Login</a></li>'
    result += '    <li><a href="project">Projects</a></li>'
    result += '    <li><a href="guestbook">Guestbook</a></li>'
    result += ' </ul>'
    result += '</nav>'
    return result
