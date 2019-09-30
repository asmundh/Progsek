import web
render = web.template.render('templates/')

urls = (
    '/', 'application'
)

db = web.database(
    dbn="mysql",
    host='127.0.0.1',
    port=3306,
    user='kalle',
    pw='123p',
    db='db'
)

class application():

    def GET(self):
        name = 'Bob'
        friends = db.select('users')
        return render.index(friends)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
