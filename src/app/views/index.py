import web
import models.project
from views.utils import get_nav_bar

# Get html templates
render = web.template.render('templates/')

class Index:
    
    # Get main page
    def GET(self):
        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input(projects=None)
        project_bulk_one = []
        project_bulk_two = []
        if data.projects == 'my':
            project_bulk_one = models.project.get_projects_by_status_and_owner(str(session.userid), "open")
            project_bulk_two = models.project.get_projects_by_status_and_owner(str(session.userid), "in progress")
        elif data.projects == 'customer':
            project_bulk_one = models.project.get_projects_by_participant_and_status(str(session.userid), "open")
            project_bulk_two = models.project.get_projects_by_participant_and_status(str(session.userid), "in progress")
        elif data.projects == 'finished':
            project_bulk_one = models.project.get_projects_by_status_and_owner(str(session.userid), "finished")
            project_bulk_two = models.project.get_projects_by_participant_and_status(str(session.userid), "finished")

        return render.index(nav, project_bulk_one, project_bulk_two, data.projects)
