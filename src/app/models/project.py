from models.database import db

def get_categories():
    """
    Get all categories

        :return: List of categories
    """
    cursor = db.cursor()
    query = ("SELECT * FROM project_category")
    cursor.execute(query)
    categories = cursor.fetchall()
    cursor.close()
    return categories

def set_project(categoryid, userid, project_title, project_description, project_status):
    """
    Store a project in the database

        :param categoryid: The id of the corresponding category
        :param userid: The id of the project owner
        :param project_title: The title of the project
        :param project_description: The project description
        :param project_status: The status of the project
        :type categoryid: str
        :type userid: str
        :type project_title: str
        :type project_description: str 
        :type project_status: str
        :return: The id of the new project
    """
    cursor = db.cursor()
    query = ("INSERT INTO projects VALUES (NULL, \"" + 
        categoryid + "\", \"" + userid + "\", \"" + project_title + "\", \"" + 
        project_description + "\", \"" + project_status + "\")")
    cursor.execute(query)
    db.commit()
    cursor.close()
    users_projects = get_projects_by_owner(userid) 
    projectid = users_projects[-1][0]
    return projectid

def get_project_by_id(projectid):
    """
    Retrieve a project by its id
        :param projectid: The project id
        :type projectid: str
        :return: The selected project
    """
    cursor = db.cursor()
    query = ("SELECT * FROM projects WHERE projectid = \"" + 
        projectid + "\"")
    cursor.execute(query)
    project = cursor.fetchall()
    return project[0]

def get_projects_by_status_and_category(categoryid, project_status):
    """
    Retrieve all projects from a category with a specific status

        :param catergoryid: The id of the category
        :param project_status: The status to filter on
        :type catergoryid: str
        :type project_status: str
        :return: A list of projects
    """
    cursor = db.cursor()
    query = ("SELECT * FROM projects WHERE project_status = \"" + 
        project_status + "\" AND categoryid = \"" + categoryid + "\"")
    cursor.execute(query)
    projects = cursor.fetchall()
    return projects

def get_projects_by_owner(userid):
    cursor = db.cursor()
    query = ("SELECT * FROM projects WHERE userid = \"" + userid + "\"")
    cursor.execute(query)
    projects = cursor.fetchall()
    return projects

def get_projects_by_status_and_owner(userid, project_status):
    """
    Retrieve all projects owned by a user with a specific status

        :param userid: The id of the owner
        :param project_status: The status to filter on
        :type userid: str
        :type project_status: str
        :return: A list of projects
    """
    cursor = db.cursor()
    query = ("SELECT * FROM projects WHERE project_status = \"" + 
        project_status + "\" AND userid = \"" + userid + "\"")
    cursor.execute(query)
    projects = cursor.fetchall()
    return projects

def get_projects_by_participant_and_status(userid, project_status):
    """
    Retrieve all projects where the user is a participant with specific status

        :param userid: The id of the participant
        :param project_status: The status to filter on
        :type userid: str
        :type project_status: str
        :return: A list of projects
    """
    cursor = db.cursor()
    query = ("SELECT * FROM projects, projects_users WHERE projects.project_status = \"" + 
        project_status + "\" AND projects_users.userid = \"" + userid + 
        "\" AND projects_users.projectid = projects.projectid")
    cursor.execute(query)
    projects = cursor.fetchall()
    return projects

def set_task(projectid, task_title, task_description, budget):
    """
    Create a task

        :param projectid: The corresponding project id
        :param task_title: The title of the task
        :param task_description: The description of the task
        :param budget: The task budget
        :type projectid: str
        :type task_title: str
        :type task_description: str
        :type budget: str
    """
    cursor = db.cursor()
    query = ("INSERT INTO tasks (projectid, title, task_description, budget, task_status) VALUES (\"" +
        projectid + "\", \"" + task_title + "\", \"" +
        task_description + "\", \"" + budget + "\", \"waiting for delivery\")")
    cursor.execute(query)
    db.commit()
    cursor.close

def get_tasks_by_project_id(projectid):
    """
    Get all tasks belonging to a project

        :param project_id: The id of the project holding the tasks
        :type project_id: str
        :return: List of tasks
    """
    cursor = db.cursor()
    query = ("SELECT * FROM tasks WHERE projectid = \"" + projectid + "\"")
    cursor.execute(query)
    tasks = cursor.fetchall()
    cursor.close
    return tasks

def set_task_file(taskid, filename):
    cursor = db.cursor()
    query = ("INSERT INTO task_files (taskid, filename) VALUES (\"" + 
        taskid + "\", \"" + filename + "\")")
    print(query)
    cursor.execute(query)
    db.commit()
    cursor.close()

def get_task_files(taskid):
    cursor = db.cursor()
    query = ("SELECT filename FROM task_files WHERE taskid = \"" + str(taskid) + "\"")
    cursor.execute(query)
    filenames = cursor.fetchall()
    print(query)
    print(filenames)
    cursor.close
    return filenames

def set_projects_user(projectid, userid, read_permission="TRUE", 
        write_permission="NULL", modify_permission="NULL"):
    cursor = db.cursor()
    query = ("INSERT INTO projects_users VALUES (\"" + projectid + "\", \"" + 
        userid + "\", " + read_permission + ", " + 
        write_permission + ", " + modify_permission + ")")
    cursor.execute(query)
    db.commit()
    cursor.close()
