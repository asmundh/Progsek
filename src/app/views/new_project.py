import web
from views.forms import get_task_form_elements, get_new_project_form, get_project_form_elements, get_user_form_elements, project_buttons
import models.project
import models.login
from views.utils import get_nav_bar

# Get html templates
render = web.template.render('templates/')

class New_project:

    def GET(self):
        """
        Get the project registration form
            
            :return: New project page
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        project_form_elements = get_project_form_elements()
        task_form_elements = get_task_form_elements()
        user_form_elements = get_user_form_elements()
        project_form = get_new_project_form((project_form_elements + task_form_elements + user_form_elements))
        return render.new_project(nav, project_form, project_buttons,  "")

    def POST(self):
        """
        Create a new project

            :return: Redirect to main page
        """            
        session = web.ctx.session
        nav = get_nav_bar(session)

        # Try the different URL input parameters to determine how to generate the form
        data = web.input(add_user=None, remove_user=None, 
            add_task=None, remove_task = None, create_project=None)

        # Add a set of task fields to the form
        if data.add_task:
            project_form = self.compose_form(data, "add_task")
            return render.new_project(nav, project_form, project_buttons,  "") 
        
        # Remove a set of task fields from the form
        if data.remove_task:
            project_form = self.compose_form(data, "remove_task")
            return render.new_project(nav, project_form, project_buttons,  "")     
        
        if data.add_user:
            project_form = self.compose_form(data, "add_user")
            return render.new_project(nav, project_form, project_buttons,  "")     
        
        if data.remove_user:
            project_form = self.compose_form(data, "remove_user")
            return render.new_project(nav, project_form, project_buttons,  "")    
            
        # Post the form data and save the project in the database
        if data.create_project:
                            
            project_form = self.compose_form(data, None)
            if not project_form.validates():
                return render.new_project(nav, project_form, project_buttons,  "")    

            task_count = get_task_count(data)
            user_count = get_user_count(data)

            # If there already are users assignet to the project the status will be set to in progress
            status = "open"
            if len(data.user_name_0):
                status = "in progress"

            # Validate the input user names
            for i in range(0, user_count):
                if len(data["user_name_"+str(i)]) and not models.login.get_user_id_by_name(data["user_name_"+str(i)]):    
                    return render.register(nav, project_form, project_buttons,  "Invalid user: " + data["user_name_"+str(i)])

            # Save the project to the database
            projectid = models.project.set_project(data.category_name, str(session.userid), 
            data.project_title, data.project_description, status)

            # Save the tasks in the database
            for i in range(0, task_count):
                models.project.set_task(str(projectid), (data["task_title_" + str(i)]), 
                (data["task_description_" + str(i)]), (data["budget_" + str(i)]))
                                
            # Save the users in the database
            for i in range(0, user_count):
                    if len(data["user_name_"+str(i)]):
                        userid = models.login.get_user_id_by_name(data["user_name_"+str(i)])
                        read, write, modify = "FALSE", "FALSE", "FALSE"
                        try:
                            data["read_permission_"+str(i)]
                            read = "TRUE"
                        except Exception as e:
                            read = "FALSE"
                            pass
                        try:
                            data["write_permission_"+str(i)]
                            write = "TRUE"
                        except Exception as e:
                            write = "FALSE"
                            pass
                        try:
                            data["modify_permission_"+str(i)]
                            modify = "TRUE"
                        except Exception as e:
                            # This error will be raised if no permission is set
                            modify = "FALSE"
                            raise e
                        
                        models.project.set_projects_user(str(projectid), str(userid), read, write, modify)
                        
            raise web.seeother('/?projects=my')
                        
    def compose_form(self, data, operation):
        """
        Compose a new project form by adding or removing a task

            :param data: The data object from web.input
            :param add: True or False
            :type add: boolean
            :return: A complete project form object
        """
        task_count = get_task_count(data)
        user_count = get_user_count(data)
        print(user_count)
        if operation == "remove_task" and task_count > 1:
            task_count -= 1

        if operation == "remove_user" and user_count >=1:
            user_count -= 1
        
        project_form_elements = get_project_form_elements(data.project_title, data.project_description, data.category_name)
        task_form_elements = ()
        user_form_elements = ()

        for i in range(0, task_count):
            old_task_form_element = get_task_form_elements(i, data["task_title_"+str(i)], 
            data["task_description_"+str(i)], data["budget_"+str(i)])
            task_form_elements = (task_form_elements + old_task_form_element)

        for i in range(0, user_count):

            try:
                old_user_form_element = get_user_form_elements(i, data["user_name_"+str(i)],
                data["read_permission_"+str(i)], data["write_permission_"+str(i)], data["modify_permission_"+str(i)])
                user_form_elements = (user_form_elements + old_user_form_element)
            except Exception as e:
                try:
                    old_user_form_element = get_user_form_elements(i, data["user_name_"+str(i)],
                    data["read_permission_"+str(i)], data["write_permission_"+str(i)])
                    user_form_elements = (user_form_elements + old_user_form_element)
                    pass
                except Exception as e:
                    try:
                        old_user_form_element = get_user_form_elements(i, data["user_name_"+str(i)],
                        data["read_permission_"+str(i)])
                        user_form_elements = (user_form_elements + old_user_form_element)
                        pass
                    except Exception as e:
                        try:
                            old_user_form_element = get_user_form_elements(i, data["user_name_"+str(i)])
                            user_form_elements = (user_form_elements + old_user_form_element)
                            pass
                        except Exception as e:
                            raise e

        if operation == "add_task":
            new_task_form_elements = get_task_form_elements(task_count)    
            project_form = get_new_project_form((project_form_elements + task_form_elements + new_task_form_elements + user_form_elements))
            return project_form

        if operation == "add_user":
            new_user_form_elements = get_user_form_elements(user_count)
            project_form = get_new_project_form((project_form_elements + task_form_elements + user_form_elements + new_user_form_elements))
            return project_form

        project_form = get_new_project_form((project_form_elements + task_form_elements + user_form_elements))
        return project_form
        
                        
def get_task_count(data):
    """
    Determine the number of tasks created by removing 
    the four other elements from count and divide by the 
    number of variables in one task.
     
        :param data: The data object from web.input
        :return: The number of tasks opened by the client
    """
    task_count = 0
    while True:
        try:
            data["task_title_"+str(task_count)]
            task_count += 1
        except:
            break
    return task_count

def get_user_count(data):
    user_count = 0
    while True:
        try:
            data["user_name_"+str(user_count)]
            user_count += 1
        except:
            break
    return user_count