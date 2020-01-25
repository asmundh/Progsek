from models.database import db
import mysql.connector

def get_users():
    """
    Retreive all registrered users from the database
        :return: users
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT userid, username from users")
    try:
        cursor.execute(query)
        users = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        users = []
        exit(1)
    finally:
        cursor.close()
        db.close()
    return users

def get_user_id_by_name(username):
    """
    Get the id of the unique username
        :param username: Name of the user
        :return: The id of the user
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT userid from users WHERE username =\"" + username + "\"")
    cursor.execute(query)
    try:
        userid = cursor.fetchall()[0][0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        userid = None
        exit(1)
    finally:
        cursor.close()
        db.close()
    return userid

def get_user_name_by_id(userid):
    """
    Get username from user id
        :param userid: The id of the user
        :return: The name of the user
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT username from users WHERE userid =\"" + userid + "\"")
    cursor.execute(query)
    try:
        username = cursor.fetchall()[0][0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        username = None
        exit(1)
    finally:
        cursor.close()
        db.close()
    cursor.close()
    return username

def match_user(username, password):
    """
    Check if user credentials are correct, return if exists

        :param username: The user attempting to authenticate
        :param password: The corresponding password
        :type username: str
        :type password: str
        :return: user
    """
    db.connect()
    cursor = db.cursor()
    query = ("SELECT userid, username from users where username = \"" + username + 
            "\" and password = \"" + password + "\"")
    cursor.execute(query)
    try:
        user = cursor.fetchall()[0]
    except mysql.connector.Error as err:
        print("Failed executing query: {}".format(err))
        user = None
        exit(1)
    finally:
        cursor.close()
        db.close()
    return user

        
    

