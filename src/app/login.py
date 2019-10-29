import web
from forms import login_form
import model
from utils import get_nav_bar

# Get html templates
render = web.template.render('templates/')

class Login():

    def GET(self):
        session = web.ctx.session
        # Show other registered users if the user is logged in
        if session.username:
            friends = model.get_users()
        else:
            friends = [[],[]]
        nav = get_nav_bar(session)
        return render.login(nav, login_form, friends)

    # Log In
    def POST(self):
        session = web.ctx.session
        # Validate login credential with database query
        data = web.input()
        user = model.match_user(data.username, data.password)
        # If there is a matching user/password in the database the user is logged in
        if len(user):
            friends = model.get_users()
            session.username = data.username
        else:
            friends = [[],[]]
        nav = get_nav_bar(session)
        return render.login(nav, login_form, friends)

