import web
from views.forms import login_form
import models.login
from views.utils import get_nav_bar
import os, hmac, base64, pickle, hashlib
from io import StringIO

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
        if session.username:
            friends = models.login.get_users()
        else:
            friends = [[],[]]
        nav = get_nav_bar(session)
        if 1 == 1:
            print(web.cookies())

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
            print('remember me')
            
            web.setcookie('remember', self.rememberme())
        else:
            friends = [[],[]]
        nav = get_nav_bar(session)
        return render.login(nav, login_form, friends)

    def rememberme(self):
        session = web.ctx.session
        creds = [session.username , self.sign() ]
        print(creds)
        return base64.b64encode(pickle.dumps(creds))

    def sign(self):
        session = web.ctx.session
        return self.sign_username(session.username)

    @classmethod
    def sign_username(self, username):
        secret = base64.b64decode(self.secret)
        print(username)
        return hmac.HMAC(secret, username.encode('utf-8')).hexdigest()
 
    @classmethod
    def valid_rememberme(self, cookie):
        userame, userid, sign = pickle.load(StringIO.StringIO(base64.b64decode(cookie)))
        if User.sign_username(user) == sign:
            return True
        return False
        
    @classmethod
    def from_rememberme(self, cookie):
        user, sign= pickle.load(StringIO.StringIO(base64.b64decode(cookie)))
        return user
