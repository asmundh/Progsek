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
        Handle input data and register new user in database

            :return: Main page
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input()

        f = register_form()
        if not f.validates():
            return render.register(nav, r, "All fields must be valid.")

        # Check if user exists
        if models.login.get_user_id_by_name(data.username):
            return render.register(nav, r, "Invalid user, already exists.")

        models.register.set_user(data.username, 
            hashlib.md5(b'TDT4237' + data.password.encode('utf-8')).hexdigest(), 
            data.full_name, data.company, data.email, data.street_address, 
            data.city, data.state, data.postal_code, data.country)
        
        return render.register(nav, register_form, "User registered!")

