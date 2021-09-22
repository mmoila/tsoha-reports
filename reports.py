from db import db

def get_filtered(args):
    sql = "SELECT A.id, A.date, A.title, A.description, C.username, B.ICAO_ident, A.created_at \
        FROM reports A LEFT JOIN locations B ON A.location_ID = B.id \
        LEFT JOIN users C ON A.user_id = C.id WHERE A.title LIKE :title AND B.ICAO_ident = UPPER(:location)"
    result = db.session.execute(sql, {"title":"%"+args["title"]+"%", "location":args["location"]})
    return result.fetchall()

def get_all():
    sql = "SELECT A.id, A.date, A.title, A.description, C.username, B.ICAO_ident, A.created_at \
        FROM reports A LEFT JOIN locations B ON A.location_ID = B.id \
        LEFT JOIN users C ON A.user_id = C.id"
    result = db.session.execute(sql)
    return result.fetchall()

def send(date, title, description, id, user_id):
    sql = "INSERT INTO reports (date, title, description, location_id, user_id, created_at) VALUES \
        (:date, :title, :description, :location, :user_id, date_trunc('minute', CURRENT_TIMESTAMP))"
    db.session.execute(
    sql, {"date":date, "title":title, "description":description, "location":id, "user_id":user_id})
    db.session.commit()
        
def get_report(id):
    sql = "SELECT A.id, title, date, B.location_name, description, \
        location_name FROM reports A, locations B WHERE \
        A.id=:id AND A.location_id = B.id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()
    
def delete(id):
    sql = "DELETE FROM reports WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()