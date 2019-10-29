import web
from forms import login_form, register_form, guestbook_form
import model
from utils import get_nav_bar

# Define application routes
urls = (
    '/', 'Index',
    '/login', 'Login',
    '/logout', 'Logout',
    '/register', 'Register',
    '/guestbook', 'Guestbook',
)
                              
# Initialize application using the web py framework
app = web.application(urls, globals())

# Get html templates
render = web.template.render('templates/')

# Workaround to use sessions with reloader (debugger) http://webpy.org/cookbook/session_with_reloader
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore("sessions"), initializer={"username": None})
    web.config._session = session
else:
    session = web.config._session

# Add session to global variables
render._add_global(session, 'session')


class Index():
    
    # Get main page
    def GET(self):
        nav = get_nav_bar(session)
        return render.index(nav)


class Login():

    def GET(self):
        # Show other registered users if the user is logged in
        if session.username:
            friends = model.get_users()
        else:
            friends = [[],[]]
        nav = get_nav_bar(session)
        return render.login(nav, login_form, friends)

    # Log In
    def POST(self):
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


class Register:

    # Get the registration form
    def GET(self):
        nav = get_nav_bar(session)
        return render.register(nav, register_form)

    # Register new user in database
    def POST(self):
        data = web.input()
        model.set_user(nav, data.username, data.password)
        raise web.seeother('/')


class Guestbook:

    # Get guestbook entries
    def GET(self):
        entries = model.get_guestbook_entries()
        nav = get_nav_bar(session)
        return render.guestbook(nav, entries, guestbook_form)

    def POST(self):
        data = web.input()
        entry = web.data()
        print(data)
        print(entry)
        model.set_guestbook_entry(data.entry)
        return web.seeother("/guestbook")

class Logout:

    # Kill session
    def GET(self):
        session.kill()
        session.username = None
        raise web.seeother('/')
