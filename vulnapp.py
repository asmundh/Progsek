import web
render = web.template.render('templates/')

urls = (
    '/', 'application'
)

class application():

    def GET(self):
        name = 'Bob'
        return render.index(name)
        
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
