from web import form

# Define the login form 
login_form = form.Form(
    form.Textbox("username", description="Username"),
    form.Password("password", description="Password"),
    form.Button("Log In", type="submit", description="Login"),
)

# Define the register form 
register_form = form.Form(
    form.Textbox("username", description="Username"),
    form.Password("password", description="Password"),
    form.Button("Register", type="submit", description="Register"),
)

# Define the guestbook form
guestbook_form = form.Form(
    form.Textbox("entry", description="Entry"),
    form.Button("Submit", type="submit", description="submit")
)

