import web
import models.project
from views.utils import get_nav_bar
import cgi, os
import cgitb; cgitb.enable()

# Get html templates
render = web.template.render('templates/')


class Project:

    def GET(self):
        """
        Show info about a single project

            :return: Project info page
        """
    
        # Get session
        session = web.ctx.session
        # Get navbar
        nav = get_nav_bar(session)

        data = web.input(projectid=0)
        if data.projectid:
            project = models.project.get_project_by_id(data.projectid)
            tasks = models.project.get_tasks_by_project_id(data.projectid)
        else:
            project = [[]]
            tasks = [[]]
        
        return render.project(nav, project[0], tasks)

    def POST(self):
        data = web.input(myfile={})

        fileitem = data['myfile']
        
        # Test if the file was uploaded
        if fileitem.filename:
            data = web.input(projectid=0)
            # strip leading path from file name to avoid 
            # directory traversal attacks
            fn = os.path.basename(fileitem.filename)

            if not os.path.isdir(('static/project' + data.projectid)):
                command = 'mkdir static/project' + data.projectid
                os.popen(command)

            open('static/project' + data.projectid + '/' + fn, 'wb').write(fileitem.file.read())
            message = 'The file "' + fn + '" was uploaded successfully'
            
        else:
            message = 'No file was uploaded'
        
        print (message)

        raise web.seeother('/project')
