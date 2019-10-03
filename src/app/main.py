import web
from web import form
import mysql.connector

urls = (
    '/', 'index'
)

db2 = mysql.connector.connect(user='root', password='root',
                              host='10.5.0.5',
                              database='db')
                              
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
        cursor = db2.cursor()
        query = ("SELECT userid, username from users")
        cursor.execute(query)
        friends = cursor.fetchall()        
        return render.index(login_form, friends)


if __name__ == "__main__":
    app.run()

application = app.wsgifunc()
