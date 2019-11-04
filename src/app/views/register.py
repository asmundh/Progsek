import web
from views.forms import register_form
import models.register
from views.utils import get_nav_bar

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
        models.register.set_user(data.username, data.password, 
        data.full_name, data.company, data.phone_number, data.street_address, 
        data.city, data.state, data.postal_code, data.country)
        raise web.seeother('/')

