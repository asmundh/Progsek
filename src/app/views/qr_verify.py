import web
from views.forms import qr_verify_form
import models.user
from views.utils import get_nav_bar
import sys, os, hmac, base64, pickle
import hashlib
from authenticator.authenticator import validate_key
from views.login import Login
from uuid import uuid4
from logs.log import write_requests as log

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
        session.csrf_token = uuid4().hex
        return render.qr_verify(session.auth_url, qr_verify_form, "", session.csrf_token)

    def POST(self):
        """
        Renders an authorization page to be scanned by google authorizer app
        :return:
        """
        session = web.ctx.session
        session.auth = False
        data = web.input(key="")

        inp = web.input()
        if not ('csrf_token' in inp and inp.csrf_token == session.pop('csrf_token', None)):
            raise web.badrequest()

        # Check if inputted is correct
        validated = validate_key(session.unauth_username, data.key)
        if not validated:
            log("TWO-FACTOR", web.ctx['ip'], [('Username',session.unauth_username), ("Key", data.key), ("Response: ", "Login failed, auth key is wrong")])
            session.csrf_token = uuid4().hex
            return render.qr_verify(session.auth_url, qr_verify_form, "Wrong authenticator code", session.csrf_token) 
        if validated:
            log("TWO-FACTOR", web.ctx['ip'], [('Username',session.unauth_username), ("Key", data.key), ("Response: ", "Login OK, auth key correct")])
            Login.login(session.unauth_userid, session.unauth_username, session.unauth_remember)
            raise web.seeother("/")
