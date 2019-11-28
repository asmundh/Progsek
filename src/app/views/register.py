import web
from views.forms import register_form
import models.register
import models.login
from views.utils import get_nav_bar
import hashlib
import re

# Get html templates
render = web.template.render('templates/')


class Register:

    def GET(self):
        """
        Get the registration form

            :return: A page with the registration form
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        return render.register(nav, register_form, "")

    def POST(self):
        """
        Register new user in database

            :return: Main page
        """
        session = web.ctx.session

        nav = get_nav_bar(session)

        data = web.input()
        
        message = ""

        if models.login.get_user_id_by_name(data.username):
            message += "Invalid user, already exists. "

        if not re.match(r"[^@]+@[^@]+\.[^@]+", data.email):
            message += "Invalid email address. "

        if not len(data.password) > 5:
            message += "Invalid password, must be atleast 6 characters long. "

        if len(message) == 0:
            models.register.set_user(data.username, hashlib.md5(b'TDT4237' + data.password.encode('utf-8')).hexdigest(), 
            data.full_name, data.email, data.company, data.phone_number, data.street_address, 
            data.city, data.state, data.postal_code, data.country)
            message += "User Registered. "

        
        return render.register(nav, register_form, message)

