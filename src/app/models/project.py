from models.database import db

def get_categories():
    cursor = db.cursor()
    query = ("SELECT * FROM project_category")
    cursor.execute(query)
    categories = cursor.fetchall()
    cursor.close()
    return categories

def set_project(categoryid, userid, project_title, project_description, project_status):
    cursor = db.cursor()
    query = ("INSERT INTO projects VALUES (NULL, \"" + 
        categoryid + "\", \"" + userid + "\", \"" + project_title + "\", \"" + 
        project_description + "\", \"" + project_status + "\")")
    cursor.execute(query)
    db.commit()
    cursor.close()
    projectid = get_projects_by_status_and_owner(userid, "open")[-1][0]
    return projectid

def get_project_by_id(projectid):
    cursor = db.cursor()
    query = ("SELECT * FROM projects WHERE projectid = \"" + 
        projectid + "\"")
    cursor.execute(query)
    project = cursor.fetchall()
    return project

def get_projects_by_status_and_category(categoryid, project_status):
    cursor = db.cursor()
    query = ("SELECT * FROM projects WHERE project_status = \"" + 
        project_status + "\" AND categoryid = \"" + categoryid + "\"")
    cursor.execute(query)
    projects = cursor.fetchall()
    return projects

def get_projects_by_status_and_owner(userid, project_status):
    cursor = db.cursor()
    query = ("SELECT * FROM projects WHERE project_status = \"" + 
        project_status + "\" AND userid = \"" + userid + "\"")
    cursor.execute(query)
    projects = cursor.fetchall()
    return projects

def get_projects_by_participant_and_status(userid, project_status):
    cursor = db.cursor()
    query = ("SELECT * FROM projects, projects_users WHERE projects.project_status = \"" + 
        project_status + "\" AND projects_users.userid = \"" + userid + 
        "\" AND projects_users.projectid = projects.projectid")
    cursor.execute(query)
    projects = cursor.fetchall()
    return projects

def set_task(projectid, task_title, task_description, budget):
    cursor = db.cursor()
    query = ("INSERT INTO tasks (projectid, title, task_description, budget, task_status) VALUES (\"" +
    projectid + "\", \"" + task_title + "\", \"" +
    task_description + "\", \"" + budget + "\", \"waiting for delivery\")")
    cursor.execute(query)
    db.commit()

