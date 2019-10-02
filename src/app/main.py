import web
from web import form


urls = (
    '/', 'index'
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
        #friends = db.select('users')
        return render.index(login_form)


if __name__ == "__main__":
    app.run()

application = app.wsgifunc()
