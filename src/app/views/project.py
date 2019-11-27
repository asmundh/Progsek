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

        permissions = models.project.get_user_permissions(str(session.userid), data.projectid)

        if data.projectid:
            project = models.project.get_project_by_id(data.projectid)
            tasks = models.project.get_tasks_by_project_id(data.projectid)
        else:
            project = [[]]
            tasks = [[]]
        render = web.template.render('templates/', globals={'get_task_files':models.project.get_task_files, 'session':session})
        return render.project(nav, project, tasks,permissions)

    def POST(self):
        # Get session
        session = web.ctx.session

        data = web.input(myfile={}, deliver=None)

        fileitem = data['myfile']

        permissions = models.project.get_user_permissions(str(session.userid), data.projectid)
        print(data.deliver)
        # Test if the file was uploaded
        if fileitem.filename:
            if not permissions[1]:
                print("Permission denied")
                raise web.seeother(('/project?projectid=' + data.projectid))

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
        elif data.deliver:
            models.project.update_task_status(data.taskid, "delivered")
            print(data.taskid)
        else:
            message = 'No file was uploaded'
        

        raise web.seeother(('/project?projectid=' + data.projectid))

