import web
from views.utils import get_nav_bar

# Get html templates
render = web.template.render('templates/')


class Logout:

    def GET(self):
        """
        Log out of the application (kill session and reset variables)
            :return: Redirect to main page
        """
        session = web.ctx.session
        session.kill()
        session.username = None
        session.id = None
        raise web.seeother('/')
