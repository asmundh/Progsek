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
        print("HELLO")
        # Get session
        session = web.ctx.session

        data = web.input(myfile={}, deliver=None, accepted=None, declined=None)

        fileitem = data['myfile']
        

        permissions = models.project.get_user_permissions(str(session.userid), data.projectid)
        tasks = models.project.get_tasks_by_project_id(data.projectid)

        print(data)
        all_tasks_accepted = True
        task_waiting = False
        task_delivered = False
        for task in tasks:
            print("TASK", task)
            print("taskid", data.taskid, "equal", task[0])
            if task[0] == int(data.taskid):  
                print("ASDASADSSD", task[6])  
                if(task[6] == "waiting for delivery" or task[6] == "declined"):
                    task_waiting = True
                if(task[6] == 'accepted'):
                    task_delivered = True
                    
        print(task_waiting, task_delivered)
        # Test if the file was uploaded
        if fileitem.filename:
            if not permissions[1] or not task_waiting:
                print("Permission denied")
                raise web.seeother(('/project?projectid=' + data.projectid))

            data = web.input(projectid=0)

            fn = fileitem.filename
            print("DATA", data)
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
        elif data.deliver and not task_delivered:
            models.project.update_task_status(data.taskid, "delivered")
        elif data.accepted:
            print("accept")
            models.project.update_task_status(data.taskid, "accepted")
            print(data.taskid)
            all_tasks_accepted = True
            print("================================================")
            print("================================================")
    
            tasks = models.project.get_tasks_by_project_id(data.projectid)
            for task in tasks:
                print("task", task)
                if task[6] != "accepted":
                    all_tasks_accepted = False
            if all_tasks_accepted:
                models.project.update_project_status(str(data.projectid), "finished")

        elif data.declined:
            models.project.update_task_status(data.taskid, "declined")
        else:
            message = 'No file was uploaded'
        

        raise web.seeother(('/project?projectid=' + data.projectid))

