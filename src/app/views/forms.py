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

# Define the project form

categories = get_categories()

project_form = form.Form(
    form.Textbox("project_title", description="Title"),
    form.Textbox("project_description", description="Description"),
    form.Dropdown("category_name", args=categories),
    form.Button("Submit", type="submit", description="submit")
)

# Define the guestbook form
guestbook_form = form.Form(
    form.Textbox("entry", description="Entry"),
    form.Button("Submit", type="submit", description="submit")
)

