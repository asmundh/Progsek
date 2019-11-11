import web
from views.forms import get_task_form_elements, get_new_project_form, get_project_form_elements
import models.project
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
        project_form = get_new_project_form((project_form_elements + task_form_elements))
        return render.new_project(nav, project_form)

    def POST(self):
        """
        Create a new project

            :return: Redirect to main page
        """
        data = web.input()
        session = web.ctx.session
        nav = get_nav_bar(session)

        print(data)
        # Try the three different URL input parameters to determine how to generate the form
        try:
            # Add a set of task fields to the form
            if data["Add Task"]:
                project_form = self.compose_form(data, True)
                print("add task")
                return render.new_project(nav, project_form)
        except Exception as e: 
            try:
                # Remove a set of task fields from the form
                if data["Remove Task"]:
                    project_form = self.compose_form(data, False)
                    return render.new_project(nav, project_form)     
            except Exception as e:
                try:
                    # Post the form data and save the project in the database
                    if data["Create Project"]:
                        print("Create project")
                        projectid = models.project.set_project(data.category_name, str(session.userid), 
                        data.project_title, data.project_description, "open")
                        print("id:", projectid)
                        task_count = self.get_task_count(data)
                        print(task_count)
                        # Save the tasks in the database
                        for i in range(0, task_count):
                            models.project.set_task(str(projectid), (data["task_title_" + str(i)]), 
                            (data["task_description_" + str(i)]), (data["budget_" + str(i)]))
                        raise web.seeother('/')
                except Exception as e:
                    raise e

    def get_task_count(self, data):
        task_count = 0
        # Remove the four other elements from count and divide by the number of variables in one task.
        task_count = int((len(data) - 4) / 3)
        """while True:
            try:
                if data["task_title_"+str(task_count)] or data["task_description_"+str(task_count)] or data["task_budget_"+str(task_count)]:
                    task_count += 1
            except Exception as e:
                pass
                break"""
        return task_count

    def compose_form(self, data, add):
        task_count = self.get_task_count(data)
        # A task is either added or removed
        if not add and task_count >= 1:
                task_count -= 1
        
        project_form_elements = get_project_form_elements(data.project_title, data.project_description, data.category_name)
        task_form_elements = ()
        old_task_form_element = ()

        for i in range(0, task_count):
            old_task_form_element = get_task_form_elements(i, data["task_title_"+str(i)], 
            data["task_description_"+str(i)], data["budget_"+str(i)])
            task_form_elements = (task_form_elements + old_task_form_element)

        if add:
            new_task_form_elements = get_task_form_elements(task_count)    
            project_form = get_new_project_form((project_form_elements + task_form_elements + new_task_form_elements))
        else:
            project_form = get_new_project_form((project_form_elements + task_form_elements))
        return project_form
        
