import web
from web import form
import mysql.connector

# Define application routes
urls = (
    '/', 'index',
    '/logout', 'logout',
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

    login_form = form.Form(
        form.Textbox("username", description="Username"),
        form.Password("password", description="Password"),
        form.Button("submit", type="submit", description="Login"),
    )

    def GET(self):
        cursor = db.cursor()
        query = ("SELECT userid, username from users")
        cursor.execute(query)
        friends = cursor.fetchall()
        cursor.close()
        return render.index(self.login_form, friends)

    def POST(self):
        cursor = db.cursor()
        query = ("SELECT userid, username, password from users")
        cursor.execute(query)
        friends = cursor.fetchall()
        cursor.close()
        data = web.input()
        print("name:", data.username)
        for user in friends:
            if data.username == user[1] and data.password == user[2]:
                session.username = data.username
                return render.index(self.login_form, friends[:2])


class logout:

    def GET(self):
        session.kill()
        return "Logged out"

if __name__ == "__main__":
    app.run()

application = app.wsgifunc()
