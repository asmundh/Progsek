import web
import mysql.connector
from forms import login_form, register_form

# Define application routes
urls = (
    '/', 'index',
    '/logout', 'logout',
    '/register', 'register',
)

# Access datavase using mysql connector package
db = mysql.connector.connect(
    user='root', 
    password='root',
    host='10.5.0.5',
    database='db'
)
                              
# Initialize application using the web py framework
app = web.application(urls, globals())

# Get html templates
render = web.template.render('templates/')

# Workaround to use sessions with reloader (debugger) http://webpy.org/cookbook/session_with_reloader
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore("sessions"), initializer={"username": None})
    web.config._session = session
else:
    session = web.config._session

# Add session to global variables
render._add_global(session, 'session')

class index():

    # Get main page
    def GET(self):
        # Show other registered users if the user is logged in
        if session.username:
            cursor = db.cursor()
            query = ("SELECT userid, username from users")
            cursor.execute(query)
            friends = cursor.fetchall()
            cursor.close()
        else:
            friends = [[],[]]
        return render.index(login_form, friends)

    # Log In
    def POST(self):
        # Validate login credential with database query
        cursor = db.cursor()
        query = ("SELECT userid, username from users where username = (%s) and password = (%s)")
        data = web.input()
        cursor.execute(query, (data.username, data.password))
        friends = cursor.fetchall()
        # If there is a matching user/password in the database the user is logged in
        if len(friends) == 1:
            query = ("SELECT userid, username from users")
            cursor.execute(query)
            friends = cursor.fetchall()
            session.username = data.username
            cursor.close()
            return render.index(login_form, friends)
        cursor.close()


class register:

    # Get the registration form
    def GET(self):
        return render.register(register_form)

    # Register new user in database
    def POST(self):
        cursor = db.cursor()
        query = ("INSERT INTO users VALUES (NULL, (%s), (%s))")
        data = web.input()
        cursor.execute(query, (data.username, data.password))
        cursor.close()
        return render.register(register_form)


class logout:

    # Kill session
    def GET(self):
        session.kill()
        return "Logged Out"
