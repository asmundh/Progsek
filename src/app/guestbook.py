import web
from forms import guestbook_form
import model
from utils import get_nav_bar

# Get html templates
render = web.template.render('templates/')



class Guestbook:

    # Get guestbook entries
    def GET(self):
        entries = model.get_guestbook_entries()
        session = web.ctx.session
        nav = get_nav_bar(session)
        return render.guestbook(nav, entries, guestbook_form)

    def POST(self):
        data = web.input()
        entry = web.data()
        print(data)
        print(entry)
        model.set_guestbook_entry(data.entry)
        return web.seeother("/guestbook")
