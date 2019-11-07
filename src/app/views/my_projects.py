import web
from views.utils import get_nav_bar
from views.project import Project
from models.project import get_categories, get_projects_by_status_and_category

# Get html templates
render = web.template.render('templates/')

class My_projects:
    
    # Get projects
    def GET(self):
        session = web.ctx.session
        data = web.input(categoryid=0)
        open_projects=[]
        if data.categoryid != 0:
            open_projects = get_projects_by_status_and_category(data.categoryid, "open")
        nav = get_nav_bar(session)
        categories = get_categories()
        return render.my_projects(nav, categories, open_projects)
