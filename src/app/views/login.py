import web
from views.forms import login_form
import models.login
from views.utils import get_nav_bar

# Get html templates
render = web.template.render('templates/')

class Login():

    def GET(self):
        """
        Show the login page
            
            :return: The login page showing other users if logged in
        """
        session = web.ctx.session
        if session.username:
            friends = models.login.get_users()
        else:
            friends = [[],[]]
        nav = get_nav_bar(session)
        return render.login(nav, login_form, friends)

    def POST(self):
        """
        Log in to the web application and register the session
            :return:  The login page showing other users if logged in
        """
        session = web.ctx.session
        # Validate login credential with database query
        data = web.input()
        user = models.login.match_user(data.username, data.password)
        # If there is a matching user/password in the database the user is logged in
        if len(user):
            friends = models.login.get_users()
            session.username = user[0][1]
            session.userid = user[0][0]
        else:
            friends = [[],[]]
        nav = get_nav_bar(session)
        return render.login(nav, login_form, friends)

