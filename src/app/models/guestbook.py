from models.database import db

def get_guestbook_entries():
    cursor = db.cursor()
    query = ("SELECT entryid, text FROM guestbook")
    cursor.execute(query)
    entries = cursor.fetchall()
    cursor.close()
    return entries

def set_guestbook_entry(entry):
    cursor = db.cursor()
    query = ("INSERT INTO guestbook VALUES (NULL, \"" + entry + "\")")
    cursor.execute(query)
    db.commit()
    cursor.close()

    
