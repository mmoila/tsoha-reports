from db import db

def get_all():
    sql = "SELECT * FROM reports"
    result = db.session.execute(sql)
    return result.fetchall()

def send(title, description, id):
    sql = "INSERT INTO reports (title, description, location_id) VALUES \
        (:title, :description, :location)"
    db.session.execute(
    sql, {"title":title, "description":description, "location":id})
    db.session.commit()
        

    