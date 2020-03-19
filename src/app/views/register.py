import web
from views.forms import register_form
import models.register
import models.user
from views.utils import get_nav_bar, hash_password, validate_password
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

        register = register_form()
        if not register.validates():
            return render.register(nav, register, "All fields must be valid.")

        # Check if user exists
        if models.user.get_user_id_by_name(data.username):
            return render.register(nav, register, "Invalid user, already exists.")

        # Check if password is strong enough
        password_checked_if_valid = validate_password(data.password, [data.username, data.full_name, data.company, data.email, data.street_address, data.city, data.state, data.country])
        password_feedback = password_checked_if_valid[1]
        print(data.password+" invalid because: "+password_feedback)

        if not password_checked_if_valid[0]:
            return render.register(nav, register, "Password: "+str(password_feedback))

        models.register.set_user(data.username,
                                 hash_password(data.password),
                                 data.full_name, data.company, data.email, data.street_address,
                                 data.city, data.state, data.postal_code, data.country)

        return render.register(nav, register_form, "User registered!")
