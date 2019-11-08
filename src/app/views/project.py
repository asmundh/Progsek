import web
import models.project
from views.utils import get_nav_bar

# Get html templates
render = web.template.render('templates/')


class Project:

    # Get main page
    def GET(self):
        # Get session
        session = web.ctx.session

         # Get navbar
        nav = get_nav_bar(session)
        data = web.input()
        
        return render.project(nav)
