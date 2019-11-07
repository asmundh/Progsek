from web import form
from models.project import get_categories 

# Define the login form 
login_form = form.Form(
    form.Textbox("username", description="Username"),
    form.Password("password", description="Password"),
    form.Button("Log In", type="submit", description="Login"),
)

# Define the register form 
register_form = form.Form(
    form.Textbox("username", description="Username"),
    form.Textbox("full_name", description="Full name"),
    form.Textbox("company", description="Company"),
    form.Textbox("phone_number", description="Phone Number"),
    form.Textbox("street_address", description="Street address"),
    form.Textbox("city", description="City"),
    form.Textbox("state", description="State"),
    form.Textbox("postal_code", description="Postal code"),
    form.Textbox("country", description="Country"),
    form.Password("password", description="Password"),
    form.Button("Register", type="submit", description="Register"),
)

# Define the project form elements
categories = get_categories()

# Define the task form elements
def get_task_form_elements(count=0, task_title="", task_description="", budget=""):
    task_form_elements = (
        form.Textbox("task_title_" + str(count), description="Title", value=task_title),
        form.Textarea("task_description_" + str(count), description="Description", value=task_description),
        form.Textbox("budget_" + str(count), description="Budget", value=budget)
    )
    return task_form_elements

def get_project_form_elements(project_title="", project_description="", category_name=""):
    project_form_elements = (
    form.Textbox("project_title", description="Title", value=project_title),
    form.Textarea("project_description", description="Description", value=project_description),
    form.Dropdown("category_name", description="Category Name", args=categories)
    #form.Button("Submit", type="submit", description="submit")
    )
    return project_form_elements

def get_new_project_form(elements):
    return form.Form(*elements, 
    form.Button("Add Task", type="submit", description="Add Task", value = "add_task"),
    form.Button("Remove Task", type="submit", description="Remove Task ", value = "remove_task"),
    form.Button("Create Project", type="submit", description="Create Project", value = "create_project")
    )

# Define the guestbook form
guestbook_form = form.Form(
    form.Textbox("entry", description="Entry"),

)

