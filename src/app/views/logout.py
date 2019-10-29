import web
from views.utils import get_nav_bar

# Get html templates
render = web.template.render('templates/')


class Logout:

    # Kill session
    def GET(self):
        session = web.ctx.session
        session.kill()
        session.username = None
        raise web.seeother('/')
