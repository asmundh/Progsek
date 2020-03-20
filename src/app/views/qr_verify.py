import web
from views.forms import qr_verify_form
import models.user
from views.utils import get_nav_bar
import sys, os, hmac, base64, pickle
import hashlib
from authenticator.authenticator import validate_key
from views.login import Login

# Get html templates
render = web.template.render('templates/')


class QRVerify():
    # Get the server secret to perform signatures
    secret = web.config.get('session_parameters')['secret_key']

    def GET(self):
        """
        Show the verify_qr page

            :return: The verify_qr page showing other users if logged in
        """
        session = web.ctx.session

        return render.qr_verify(session.auth_url, qr_verify_form, "")

    def POST(self):
        """
        Renders an authorization page to be scanned by google authorizer app
        :return:
        """
        session = web.ctx.session
        session.auth = False
        data = web.input(key="")

        # Check if inputted is correct
        validated = validate_key(session.unauth_username, data.key)
        if not validated: 
            return render.qr_verify(session.auth_url, qr_verify_form, "Wrong authenticator code") 
        if validated:
            Login.login(session.unauth_userid, session.unauth_username, session.unauth_remember)
            raise web.seeother("/")
