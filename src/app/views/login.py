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

        # If the user selected 'remember me' they log in automatically
        try:
            print("secret" ,self.secret)
            cookies = web.cookies()
            print("cookie", cookies)
            remember_hash = bytes(cookies.remember[2:][:-1], 'ascii')
            print("remember_hash")
            print(remember_hash)
            print(remember_hash == b'gANdcQAoWCAAAAAxN2UxZWJmOGJiODhkNzdmZWNjM2E5MmYxMTFkMjU4OHEBWAUAAABhZG1pbnECZS4=')

            encode = base64.b64decode(remember_hash)
            print("dencode", encode)

            username, sign = pickle.loads(encode)


            if self.sign_username(username) == sign:
                print("HASH MATCH")
        except Exception as e:
            raise e

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
            print('remember me')
            remember = self.rememberme()
            web.setcookie('remember', remember , 12000000)
            print("equal at start?", remember == b'gANdcQAoWCAAAAAxN2UxZWJmOGJiODhkNzdmZWNjM2E5MmYxMTFkMjU4OHEBWAUAAABhZG1pbnECZS4=')
            cookies = web.cookies()
            print("equal at start?", cookies.remember == b'gANdcQAoWCAAAAAxN2UxZWJmOGJiODhkNzdmZWNjM2E5MmYxMTFkMjU4OHEBWAUAAABhZG1pbnECZS4=')
            print(remember)
            print(cookies.remember)
            print(DeepDiff(remember, cookies.remember, 'ascii'))
        else:
            friends = [[],[]]
        nav = get_nav_bar(session)
        return render.login(nav, login_form, friends)

    def rememberme(self):
        session = web.ctx.session
        creds = [ session.username, self.sign() ]
        print(creds)
        print("save", base64.b64encode(pickle.dumps(creds)))
        return base64.b64encode(pickle.dumps(creds))

    def sign(self):
        session = web.ctx.session
        return self.sign_username(session.username)

    @classmethod
    def sign_username(self, username):
        secret = base64.b64decode(self.secret)
        print(secret)
        print(username)
        return hmac.HMAC(secret, username.encode('ascii')).hexdigest()
 
    @classmethod
    def valid_rememberme(self, cookie):
        userame, sign = pickle.load(StringIO(base64.b64decode(cookie)))
        if self.sign_username(user) == sign:
            return True
        return False
        
    @classmethod
    def from_rememberme(self, cookie):
        user, sign= pickle.load(StringIO(base64.b64decode(cookie)))
        return user
