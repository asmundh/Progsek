import web
from views.forms import login_form
import models.user
from views.utils import get_nav_bar, hash_password, verify_password
import hmac, base64
from models.user import get_user, get_user_id_by_name
import hashlib
from authenticator.authenticator import generate_qrcode, generate_url, get_key
from views.utils import get_nav_bar, hash_password, verify_password
import os, hmac, base64, pickle

from logs.log import write_requests as log
from logs.log import write_to_logins, remove_from_logins

# Get html templates


render = web.template.render('templates/')


class Login():
    # Get the server secret to perform signatures
    secret = web.config.get('session_parameters')['secret_key']

    def GET(self):
        """
        Show the login page
            
            :return: The login page showing other users if logged in
        """
        session = web.ctx.session
        nav = get_nav_bar(session)

        # Log the user in if the rememberme cookie is set and valid
        self.check_rememberme()

        return render.login(nav, login_form, "")


    def POST(self):
        """
        Log in to the web application and register the session
            :return:  The login page showing other users if logged in
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input(username="", password="", remember=False)

        # Validate login credential with database query
        user_exists = models.user.check_user_exists(data.username)

        if not user_exists:
            # Lockout if too many failed attempts
            if not (write_to_logins(str(web.ctx['ip']))):
                return render.login(nav, login_form, "- Too many login attempts in short amount of time")

            log("LOGIN", web.ctx['ip'],
                [('Username', data.username), ("Response: ", "Login failed, user does not exist")])
            return render.login(nav, login_form, "- User authentication failed")

        
        user = None
        stored_password = models.user.get_password_by_user_name(data.username)
        if (verify_password(stored_password, data.password)):
            user = models.user.match_user(data.username, stored_password)
            userid = get_user_id_by_name(data.username)
            session.unauth_username = data.username
            session.unauth_userid = userid
            session.unauth_remember = 1 if data.remember else 0
            user = get_user(session.unauth_userid)
            email = user[0][5]
            qr_verification_key = get_key(session.unauth_username)
            if qr_verification_key != None: 
                url = generate_url("beelance", email, qr_verification_key)
                session.auth_url = url
        
        user_is_verified = models.user.check_if_user_is_verified_by_username(data.username)

        # If there is a matching user/password in the database the user is logged in
        if user:
            if not user_is_verified:
                # Lockout if failed attempts
                if not (write_to_logins(str(web.ctx['ip']))):
                    return render.login(nav, login_form, "- Too many login attempts in short amount of time")

                log("LOGIN", web.ctx['ip'], [('Username', data.username), ("Password", stored_password),
                                             ("Response: ", "Login failed, User not verified")])
                return render.login(nav, login_form, "- User not verified")

            if qr_verification_key == None:
                # Lockout if failed attempts
                if not (write_to_logins(str(web.ctx['ip']))):
                    return render.login(nav, login_form, "- Too many login attempts in short amount of time")

                log("LOGIN", web.ctx['ip'], [('Username', data.username), ("Password", stored_password),
                                             ("Response: ", "Login failed, docker might have restarted")])
                return render.login(nav, login_form,
                                    "- User authentication failed. This might be because docker demon has restarted")
            else:
                log("LOGIN", web.ctx['ip'], [('Username', data.username), ("Password", stored_password),
                                             ("Response: ", "Login accepted, forwarded to two factor auth")])

                raise web.seeother("/qr_verify")
        else:
            log("LOGIN", web.ctx['ip'], [('Username', data.username), ("Password", stored_password),
                                         ("Response: ", "Login failed, username/password mismatch")])
            # Lockout if failed attempts
            if not (write_to_logins(str(web.ctx['ip']))):
                return render.login(nav, login_form, "- Too many login attempts in short amount of time")

            return render.login(nav, login_form, "- User authentication failed")

    def login(self, username, userid, remember=False):
        """
        Log in to the application
        """
        session = web.ctx.session
        session.username = username
        session.userid = session.unauth_userid

        if remember:
            rememberme = self.rememberme()
            web.setcookie('remember', rememberme, 259200)

    def check_rememberme(self):
        """
        Validate the rememberme cookie and log in
        """
        username = ""
        sign = ""
        # If the user selected 'remember me' they log in automatically
        try:
            # Fetch the users cookies if it exists
            cookies = web.cookies()
            remember_hash = hash_password(cookies)
            if verify_password(remember_hash, self.rememberme(self)):


                username, sign = remember_hash
        except AttributeError as e:
            # The user did not have the stored remember me cookie
            pass

        # If the users signed cookie matches the host signature then log in
        if self.sign_username(username) == sign:
            userid = models.user.get_user_id_by_name(username)
            self.login(username, userid, False)

    def rememberme(self):
        session = web.ctx.session
        creds = self.sign_username(session.username)
        return hash_password(creds)

    @classmethod
    def sign_username(self, username):
        """
        Sign the current users name with the hosts secret key
            :return: The users signed name
        """
        secret = base64.b64decode(self.secret)
        return hmac.HMAC(secret, username.encode('ascii')).hexdigest()
