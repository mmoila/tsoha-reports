from db import db

def get_all():
    sql = "SELECT * FROM reports"
    result = db.session.execute(sql)
    return result.fetchall()

def send(date, title, description, id):
    sql = "INSERT INTO reports (date, title, description, location_id) VALUES \
        (:date, :title, :description, :location)"
    db.session.execute(
    sql, {"date":date, "title":title, "description":description, "location":id})
    db.session.commit()
        

    