import web
import models.register
import models.user
from views.utils import get_nav_bar
import hashlib
import re

# Get html templates
render = web.template.render('templates/')

class Verify:

    def GET(self, verification_key):
        """
        Get the verification form

            :return: A page with the verification form
        """        
        user_was_verified = models.user.verify_user_by_email(verification_key)

        session = web.ctx.session
        nav = get_nav_bar(session)


        if (user_was_verified):
            return render.verify(nav, "Success", "")

        return render.verify(nav, "", "User was verified")
    
