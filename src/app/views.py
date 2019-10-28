import web
from forms import login_form, register_form, guestbook_form
import model

# Define application routes
urls = (
    '/', 'index',
    '/logout', 'logout',
    '/register', 'register',
    '/guestbook', 'guestbook',
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


class index():

    # Get main page
    def GET(self):
        # Show other registered users if the user is logged in
        if session.username:
            friends = model.get_users()
        else:
            friends = [[],[]]
        return render.index(login_form, friends)

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
        return render.index(login_form, friends)


class register:

    # Get the registration form
    def GET(self):
        return render.register(register_form)

    # Register new user in database
    def POST(self):
        data = web.input()
        model.set_user(data.username, data.password)
        raise web.seeother('/')


class guestbook:

    # Get guestbook entries
    def GET(self):
        entries = model.get_guestbook_entries()
        return render.guestbook(entries, guestbook_form)

    def POST(self):
        data = web.input()
        entry = web.data()
        print(data)
        print(entry)
        model.set_guestbook_entry(data.entry)
        return web.seeother("/guestbook")

class logout:

    # Kill session
    def GET(self):
        session.kill()
        session.username = None
        raise web.seeother('/')
