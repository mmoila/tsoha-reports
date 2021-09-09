from db import db

def get_all():
    sql = "SELECT A.id, A.date, A.title, A.description, A.user_id, B.ICAO_ident \
        FROM reports A LEFT JOIN locations B ON A.location_ID = B.id"
    result = db.session.execute(sql)
    return result.fetchall()

def send(date, title, description, id):
    sql = "INSERT INTO reports (date, title, description, location_id) VALUES \
        (:date, :title, :description, :location)"
    db.session.execute(
    sql, {"date":date, "title":title, "description":description, "location":id})
    db.session.commit()
        
def get_report(id):
    sql = "SELECT A.id, title, date, B.location_name, description, \
        location_name FROM reports A, locations B WHERE \
        A.id=:id AND A.location_id = B.id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()
    
    