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
    query = ("INSERT INTO projects values (NULL, \"1\", \"1\", \"sad\", \"desdf\", \"open\")")
    #("INSERT INTO projects values (NULL, \"" + 
    #categoryid + "\", \"" + userid + "\", \"" + title + "\", \"" + 
    #project_description + "\", \"" + project_status + "\")")
    print(query)
    cursor.execute(query)
    cursor.close()
    categories = get_categories()
    print(categories)
    return categories
    
