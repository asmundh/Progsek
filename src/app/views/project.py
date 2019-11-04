import web
from views.forms import project_form
import models.project
from views.utils import get_nav_bar

# Get html templates
render = web.template.render('templates/')

class Project:

    # Get the registration form
    def GET(self):
        session = web.ctx.session
        nav = get_nav_bar(session)
        return render.project(nav, project_form)

    # Register new user in database
    def POST(self):
        data = web.input()
        session = web.ctx.session
        print(data)
        print(session.userid)
        categories = models.project.set_project(data.category_name, str(session.userid), 
        data.project_title, data.project_description, "open")
        print(categories)
        raise web.seeother('/')
