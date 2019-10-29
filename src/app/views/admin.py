import web

class Admin:

    def GET(self):
        session = web.ctx.session
