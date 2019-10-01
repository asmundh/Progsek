import web
from web import form

# Turn of debug because sessions doesnt support it
web.config.debug = False

# Define routes
urls = (
    '/', 'application',
    "/logout", "logout",
)

# Initialize application using the web py framework
app = web.application(urls, globals())

# Enable sessions
session = web.session.Session(app, web.session.DiskStore("sessions"), initializer={"username": None})

# Get html templates
render = web.template.render('templates/')
render._add_global(session, 'session')


# Connect to database
db = web.database(
    dbn="mysql",
    host='127.0.0.1',
    port=3306,
    user='root',
    #pw='password',
    db='db'
)

class application():

    login_form = form.Form(
        form.Textbox("username", description="Username"),
        form.Password("password", description="Password"),
        form.Button("submit", type="submit", description="Login"),
    )

    def GET(self):
        friends = db.select('users')
        return render.index(self.login_form, friends)

    def POST(self):
        friends = db.select('users')
        data = web.input()
        print("name:", data.username)
        for row in friends:
            print(row)
            print(row.username)
            if data.username == row.username and data.password == row.password:
                friends = db.select('users')
                session.username = data.username
                return render.index(self.login_form, friends)

class logout:
    def GET(self):
        session.kill()
        return "Logged out"

if __name__ == "__main__":
    app.run()
