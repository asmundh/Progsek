import web
import models.project
from models.login import get_user_name_by_id
from views.utils import get_nav_bar, get_element_count
from views.forms import get_apply_form, get_user_dropdown, get_apply_permissions_form

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
        else:
            project = [[]]
            tasks = [[]]

        user_dropdown = get_user_dropdown()
        apply_form = get_apply_form(user_dropdown)
        apply_permissions_form = get_apply_permissions_form()
        applicants = [[session.userid, session.username]]
        render = web.template.render('templates/', globals={"get_apply_permissions_form":get_apply_permissions_form, 'session':session})

        return render.apply(nav, apply_form, get_apply_permissions_form, project, applicants)

    def POST(self):
        data = web.input(projectid=0, add_user=None, remove_user=None, apply=None)
        session = web.ctx.session
        nav = get_nav_bar(session)
        applicants = [session.username]
        user_dropdown = get_user_dropdown()
        apply_form = get_apply_form(user_dropdown)
        apply_permission_form = get_apply_permissions_form()
        print("POST")
        print(data)
        render = web.template.render('templates/', globals={"get_apply_permissions_form":get_apply_permissions_form, 'session':session})
        if data.projectid:
            project = models.project.get_project_by_id(data.projectid)

            if data.add_user:
                applicants = self.get_applicants(data, "add_user")
                return render.apply(nav, apply_form, get_apply_permissions_form, project, applicants)     

            elif data.remove_user:
                        applicants = self.get_applicants(data, "remove_user")
                        return render.apply(nav, apply_form, get_apply_permissions_form, project, applicants)     
            elif data.apply:
                applicants = self.get_applicants(data, "")
                for applicant in applicants:
                    models.project.set_projects_user(data.projectid, str(applicant[0]), "TRUE", "TRUE", "FALSE")
                    models.project.update_project_status(data.projectid, "in progress")
                    raise web.seeother(('/project?projectid=' + str(data.projectid)))
                    
    def get_applicants(self, data, operation):
        print(operation)
        print(data)
        user_count = get_element_count(data, "user_")
        print("count", user_count)
        applicants = []
        for i in range (0, user_count):
            print("Raw applicant", data["user_"+str(i)])
            applicant = data["user_"+str(i)][1:][:-1].split(",")
            applicants.append([ int(applicant[0]), applicant[1][2:][:-1] ])

        if operation == "remove_user":
            print("remove")
            user_to_remove = data.remove_user[1:][:-1].split(",")
            user_to_remove = [int(user_to_remove[0]), user_to_remove[1][2:][:-1]]
            for i in range (0, user_count):
                print(user_to_remove, applicants[i])
                if user_to_remove == applicants[i]:
                    applicants.pop(i)
                    break

        elif operation == "add_user":

            user_id_to_add = data.user_to_add
            user_name_to_add = get_user_name_by_id(user_id_to_add)
            new_applicant = [ int(user_id_to_add), user_name_to_add ]
            if new_applicant not in applicants:
                applicants.append(new_applicant)
        print(applicants)

        return applicants
            

