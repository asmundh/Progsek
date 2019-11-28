from web import form
from models.project import get_categories 
from models.login import get_users

# Define the login form 
login_form = form.Form(
    form.Textbox("username", description="Username"),
    form.Password("password", description="Password"),
    form.Checkbox("remember", description= "Remember me", checked=True, value=False),
    form.Button("Log In", type="submit", description="Login"),
)

# Define the register form 
register_form = form.Form(
    form.Textbox("username", description="Username"),
    form.Textbox("full_name", description="Full name"),
    form.Textbox("company", description="Company"),
    form.Textbox("email", description="Email Address"),
    form.Textbox("phone_number", description="Phone Number"),
    form.Textbox("street_address", description="Street address"),
    form.Textbox("city", description="City"),
    form.Textbox("state", description="State"),
    form.Textbox("postal_code", description="Postal code"),
    form.Textbox("country", description="Country"),
    form.Password("password", description="Password"),
    form.Button("Register", type="submit", description="Register"),
)

def get_task_form_elements(identifier=0, task_title="", task_description="", budget=""):
    """
    Generate a set of task form elements
        :param identifier: The id of the task
        :param task_title: Task title
        :param task_description: Task description 
        :param budget: Task budget
        :type identifier: int, str
        :type task_title: str
        :type task_description: str
        :type budget: int, str
        :return: A set of task form elements
    """
    task_form_elements = (
        form.Textbox("task_title_" + str(identifier), description="Title", value=task_title),
        form.Textarea("task_description_" + str(identifier), description="Description", value=task_description),
        form.Textbox("budget_" + str(identifier), description="Budget", value=str(budget))
    )
    return task_form_elements

def get_project_form_elements(project_title="", project_description="", category_name=""):
    """
    Generate a set of project form elements
        :param project_title: Project title
        :param project_description: Project description 
        :param category_name: Name of the belonging category
        :type project_title: str
        :type project_description: str
        :type category_name: str
        :return: A set of project form elements    
    """
    categories = get_categories()
    project_form_elements = (
    form.Textbox("project_title", description="Title", value=project_title),
    form.Textarea("project_description", description="Description", value=project_description),
    form.Dropdown("category_name", description="Category Name", args=categories)
    )
    return project_form_elements

def get_user_form_elements(identifier=0, user_name="", read_permission=True, write_permission=False, modify_permission=False):
    users = get_users()
    user_form_elements = (
        form.Textbox("user_name_" + str(identifier), description="User", value=user_name),        
        form.Checkbox("read_permission_" + str(identifier), description="Read Permission", checked=read_permission),
        form.Checkbox("write_permission_" + str(identifier), description="Write Permission", checked=write_permission),
        form.Checkbox("modify_permission_" + str(identifier), description="Modify Permission", checked=modify_permission)
    )
    return user_form_elements

def get_new_project_form(elements):
    """
    Combine a project form element and task elements to make a complete project form

        :param elemets: All the project and task form elements
        :return: The ready to use project form
    """
    return form.Form(*elements, 
    form.Button("Add User", type="submit", description="Add User", value="add_user"),
    form.Button("Remove User", type="submit", description="Remove User", value="remove_user"),
    form.Button("Add Task", type="submit", description="Add Task", value="add_task"),
    form.Button("Remove Task", type="submit", description="Remove Task ", value="remove_task"),
    form.Button("Create Project", type="submit", description="Create Project", value="create_project")
    )

def get_apply_form(elements):
    try:
        apply_form = form.Form(*elements,
            form.Button("Add User", type="submit", description="Add User", value="add_user"),
            form.Button("Remove User", type="submit", description="Remove User", value="remove_user"),
            form.Button("Apply", type="submit", description="Apply", value="apply")
        )
    # Exception will occur if the form only contains one element
    except TypeError as e:
        apply_form = form.Form(elements,
            form.Button("Add User", type="submit", description="Add User", value="add_user"),
            form.Button("Apply", type="submit", description="Apply", value="apply")
        )
    return apply_form

def get_user_dropdown(identifier=0):
    users = get_users()
    return form.Dropdown("user_id_" + str(identifier), description="User", args=users)
