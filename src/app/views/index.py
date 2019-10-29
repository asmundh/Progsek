import web
from views.utils import get_nav_bar
from views.guestbook import Guestbook
from views.login import Login
from views.logout import Logout
from views.register import Register
from views.admin import Admin

# Define application routes
urls = (
    '/', 'Index',
    '/login', 'Login',
    '/logout', 'Logout',
    '/register', 'Register',
    '/guestbook', 'Guestbook',
    '/admin', 'Admin',
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

# Make the session available cross modules through webctx
def session_hook():
    web.ctx.session = session
    web.template.Template.globals['session'] = session

app.add_processor(web.loadhook(session_hook))

class Index:
    
    # Get main page
    def GET(self):
        nav = get_nav_bar(session)
        return render.index(nav)
