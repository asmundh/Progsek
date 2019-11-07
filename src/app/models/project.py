from models.database import db

def get_categories():
    cursor = db.cursor()
    query = ("SELECT * FROM project_category")
    cursor.execute(query)
    categories = cursor.fetchall()
    cursor.close()
    return categories

def set_project(categoryid, userid, title, project_description, project_status):
    cursor = db.cursor()
    query = ("INSERT INTO projects VALUES (NULL, \"" + 
        categoryid + "\", \"" + userid + "\", \"" + title + "\", \"" + 
        project_description + "\", \"" + project_status + "\")")
    cursor.execute(query)
    db.commit()
    cursor.close()
    categories = get_categories()
    return categories

def get_projects_by_status_and_category(categoryid, project_status):
    cursor = db.cursor()
    query = ("SELECT * FROM projects WHERE project_status = \"" + 
        project_status + "\" AND categoryid = \"" + categoryid + "\"")
    cursor.execute(query)
    projects = cursor.fetchall()
    return projects

def set_waiting_task(projectid, title, task_description, budget):
    cursor = db.cursor()
    query = ("INSERT INTO tasks (pjojectid, title, task_description, budget) VALUES (\"" +
    projectid + "\", \"" + title + "\", \"" + title + "\", \"" +
    task_description + "\", \"" + budget + "\")")
    cursor.execute(query)

