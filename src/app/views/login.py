import web
from views.forms import login_form
import models.login
from views.utils import get_nav_bar
import os, hmac, base64, pickle, hashlib
from io import StringIO
from deepdiff import DeepDiff

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
        username = ""
        sign = ""
        # If the user selected 'remember me' they log in automatically
        try:
            # Fetch the users cookies if it exists
            cookies = web.cookies()
            # Fetch the remember cookie and convert from string to bytes
            remember_hash = bytes(cookies.remember[2:][:-1], 'ascii')
            # Decode the hash
            encode = base64.b64decode(remember_hash)
            # Load the decoded hash to receive the host signature and the username
            username, sign = pickle.loads(encode)
        except AttributeError as e:
            # The user did not have the stored remember me cookie
            pass

        # If the users signed cookie matches the host signature then log in
        if self.sign_username(username) == sign:
            userid = models.login.get_user_id_by_name(username)
            session.username = username
            session.userid = userid

        # Show a list of registered users when login in
        if session.username:
            friends = models.login.get_users()
        else:
            friends = [[],[]]
        nav = get_nav_bar(session)

        return render.login(nav, login_form, friends)

    def POST(self):
        """
        Log in to the web application and register the session
            :return:  The login page showing other users if logged in
        """
        session = web.ctx.session
        # Validate login credential with database query
        data = web.input()
        user = models.login.match_user(data.username, data.password)
        # If there is a matching user/password in the database the user is logged in
        if len(user):
            friends = models.login.get_users()
            session.username = user[0][1]
            session.userid = user[0][0]
            if data.remember:
                remember = self.rememberme()
                web.setcookie('remember', remember , 12000000)
        else:
            friends = [[],[]]
        nav = get_nav_bar(session)
        return render.login(nav, login_form, friends)

    def rememberme(self):
        """
        Encode a base64 object consisting of the username signed with the
        host secret key and the username. Can be reassembled with the
        hosts secret key to validate user.
            :return: base64 object consisting of signed username and username
        """
        session = web.ctx.session
        creds = [ session.username, self.sign_username(session.username) ]
        return base64.b64encode(pickle.dumps(creds))

    @classmethod
    def sign_username(self, username):
        """
        Sign the current users name with the hosts secret key
            :return: The users signed name
        """
        secret = base64.b64decode(self.secret)
        return hmac.HMAC(secret, username.encode('ascii')).hexdigest()
 