import web
from views.utils import get_nav_bar
from views.guestbook import Guestbook
from views.login import Login
from views.logout import Logout
from views.register import Register
from views.admin import Admin
from views.new_project import New_project
from views.open_projects import Open_projects
import models.project

# Define application routes
urls = (
    '/', 'Index',
    '/login', 'Login',
    '/logout', 'Logout',
    '/register', 'Register',
    '/guestbook', 'Guestbook',
    '/new_project', 'New_project',
    '/open_projects', 'Open_projects',
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
        data = web.input(projects=None)
        project_bulk_one = []
        project_bulk_two = []
        if data.projects == 'my':
            project_bulk_one = models.project.get_projects_by_status_and_owner(str(session.userid), "open")
            project_bulk_two = models.project.get_projects_by_status_and_owner(str(session.userid), "in progress")
        elif data.projects == 'customer':
            project_bulk_one = models.project.get_projects_by_participant_and_status(str(session.userid), "open")
            project_bulk_two = models.project.get_projects_by_participant_and_status(str(session.userid), "in progress")
        elif data.projects == 'finished':
            project_bulk_one = models.project.get_projects_by_status_and_owner(str(session.userid), "finished")
            project_bulk_two = models.project.get_projects_by_participant_and_status(str(session.userid), "finished")

        return render.index(nav, project_bulk_one, project_bulk_two, data.projects)
