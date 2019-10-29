import web
from forms import register_form
import model
from utils import get_nav_bar

# Get html templates
render = web.template.render('templates/')


class Register:

    # Get the registration form
    def GET(self):
        session = web.ctx.session
        nav = get_nav_bar(session)
        return render.register(nav, register_form)

    # Register new user in database
    def POST(self):
        data = web.input()
        model.set_user(data.username, data.password)
        raise web.seeother('/')

