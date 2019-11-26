import web
import models.project
from views.utils import get_nav_bar
import cgi, os
import cgitb; cgitb.enable()
from time import sleep

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
            # Serialize the object to make the data more read
        else:
            project = [[]]
            tasks = [[]]
        render = web.template.render('templates/', globals={'get_task_files':models.project.get_task_files})
        return render.project(nav, project[0], tasks)

    def POST(self):
        data = web.input(myfile={})

        fileitem = data['myfile']
        
        # Test if the file was uploaded
        if fileitem.filename:
            data = web.input(projectid=0)

            fn = fileitem.filename
            print(data)
            # Create the project directory if it doesnt exist
            path = 'static/project' + data.projectid
            if not os.path.isdir(path):
                command = 'mkdir ' + path
                os.popen(command)
                sleep(0.5)
            path = path + '/task' + data.taskid
            print(path)
            if not os.path.isdir(path):
                print(data.taskid)
                command = 'mkdir ' + path
                os.popen(command)
                sleep(0.5)
            open(path + '/' + fn, 'wb').write(fileitem.file.read())
            message = 'The file "' + fn + '" was uploaded successfully'
            models.project.set_task_file(data.taskid, (path + "/" + fn))
        else:
            message = 'No file was uploaded'
        
        print (message)

        raise web.seeother(('/project?projectid=' + data.projectid))

