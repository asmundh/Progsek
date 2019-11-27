import web
import models.project
from models.login import get_user_name_by_id
from views.utils import get_nav_bar
from views.forms import get_apply_form, get_user_dropdown
from views.new_project import get_user_count

# Get html templates
render = web.template.render('templates/')

class Apply:

    def GET(self):
        print("GET")
        # Get session
        session = web.ctx.session
        # Get navbar
        nav = get_nav_bar(session)

        data = web.input(projectid=0)
        if data.projectid:
            project = models.project.get_project_by_id(data.projectid)
            #tasks = models.project.get_tasks_by_project_id(data.projectid)
        else:
            project = [[]]
            tasks = [[]]
        #render = web.template.render('templates/', globals={'get_task_files':models.project.get_task_files, 'session':session})
        #render_project = render.project(nav, project[0], tasks)
        user_dropdown = get_user_dropdown()
        apply_form = get_apply_form(user_dropdown)
        applicants = [[session.userid, session.username]]
        return render.apply(nav, apply_form, project, applicants)

    def POST(self):
        data = web.input(projectid=0)
        session = web.ctx.session
        nav = get_nav_bar(session)
        applicants = [session.username]
        user_dropdown = get_user_dropdown()
        apply_form = get_apply_form(user_dropdown)
        print("POST")
        print(data)
        if data.projectid:
            project = models.project.get_project_by_id(data.projectid)
            try:
                if data["Add User"]:
                    #project_form = self.compose_form(data, "add_user")
                    applicants = self.get_applicants(data, "add_user")
                    return render.apply(nav, apply_form, project, applicants)     
            except Exception as e:
                try:
                    if data["Remove User"]:
                        #project_form = self.compose_form(data, "remove_user")
                        applicants = self.get_applicants(data, "remove_user")
                        return render.apply(nav, apply_form, project, applicants)    
                except Exception as e:
                    try:
                        if data["Apply"]:
                            applicants = self.get_applicants(data, "")
                            for applicant in applicants:
                                print("Add", applicant, data.projectid)
                                models.project.set_projects_user(data.projectid, str(applicant[0]), "TRUE", "TRUE", "FALSE")
                            raise web.seeother(('/project?projectid=' + data.projectid))
                    except Exception as e:
                        raise

    def get_applicants(self, data, operation):
        print(operation)
        print(data)
        user_count = get_user_count(data)
        print("count", user_count)
        applicants = []
        for i in range (0, user_count):
            print("Raw applicant", data["user_name_"+str(i)])
            applicant = data["user_name_"+str(i)][1:][:-1].split(",")
            applicants.append([ int(applicant[0]), applicant[1][2:][:-1] ])

        if operation == "remove_user":
            print("remove")
            user_to_remove = data["Remove User"][1:][:-1].split(",")
            user_to_remove = [int(user_to_remove[0]), user_to_remove[1][2:][:-1]]
            for i in range (0, user_count):
                print(user_to_remove, applicants[i])
                if user_to_remove == applicants[i]:
                    applicants.pop(i)
                    break

        elif operation == "add_user":

            user_id_to_add = data.user_id_0
            user_name_to_add = get_user_name_by_id(user_id_to_add)
            new_applicant = [ int(user_id_to_add), user_name_to_add ]
            if new_applicant not in applicants:
                applicants.append(new_applicant)
        print(applicants)

        return applicants
            

