import web
from web import form


urls = (
    '/', 'index'
)

# Connect to database
db = web.database(
    dbn="mysql",
    host='10.5.0.5',
    port=3306,
    user='root',
    pw='root',
    db='db'
)

# Initialize application using the web py framework
app = web.application(urls, globals())

# Get html templates
render = web.template.render('templates/')

login_form = form.Form(
    form.Textbox("username", description="Username"),
    form.Password("password", description="Password"),
    form.Button("submit", type="submit", description="Login"),
)

class index():


    def GET(self):
        friends = db.select('users')
        return render.index(login_form, friends)


if __name__ == "__main__":
    app.run()

application = app.wsgifunc()
