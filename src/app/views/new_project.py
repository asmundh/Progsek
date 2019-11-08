import web
from views.forms import get_task_form_elements, get_new_project_form, get_project_form_elements
import models.project
from views.utils import get_nav_bar

# Get html templates
render = web.template.render('templates/')

class New_project:

    # Get the registration form
    def GET(self):
        session = web.ctx.session
        nav = get_nav_bar(session)
        project_form_elements = get_project_form_elements()
        task_form_elements = get_task_form_elements()
        project_form = get_new_project_form((project_form_elements + task_form_elements))
        return render.new_project(nav, project_form)

    # Register new project in database
    def POST(self):
        data = web.input()
        session = web.ctx.session
        nav = get_nav_bar(session)

        try:
            if data["Add Task"]:
                project_form = self.compose_form(data, True)
                return render.project(nav, project_form)
        except Exception as e: 
            try:
                if data["Remove Task"]:
                    project_form = self.compose_form(data, False)
                    return render.project(nav, project_form)     
                else:
                    pass
            except Exception as e:
                try:
                    if data["Create Project"]:
                        print("Create")
                        models.project.set_waiting_task
                        
                    else:
                        pass
                except Exception as e:
                    pass

        categories = models.project.set_project(data.category_name, str(session.userid), 
        data.project_title, data.project_description, "open")
        raise web.seeother('/')

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
        
