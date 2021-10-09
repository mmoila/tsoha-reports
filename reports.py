from flask import session
from db import db

def get_filtered(args):
    if args["location"] == "" and args["title"] == "":
        return get_all()
    sql = "SELECT A.id, A.date, A.title, A.description, C.username, B.ICAO_ident, A.created_at, D.type\
        FROM reports A LEFT JOIN locations B ON A.location_ID = B.id\
        LEFT JOIN users C ON A.user_id = C.id\
        LEFT JOIN report_types D ON A.report_type = D.id WHERE"
    if args["title"] != "":
        sql += " A.title LIKE :title AND"
    if args["location"] != "":
        sql += " B.ICAO_ident LIKE UPPER(:location)"
    else: 
        sql = sql[:-3]
    result = db.session.execute(sql, {"title":"%"+args["title"]+"%", "location":args["location"]})
    return result.fetchall()

def get_all():
    sql = "SELECT A.id, A.date, A.title, A.description, C.username, B.ICAO_ident, A.created_at, D.type \
        FROM reports A LEFT JOIN locations B ON A.location_ID = B.id \
        LEFT JOIN users C ON A.user_id = C.id  \
        LEFT JOIN report_types D ON A.report_type = D.id"
    if session["admin"]:
        result = db.session.execute(sql)
    else:
        sql += " WHERE A.user_id = :user_id"
        result = db.session.execute(sql, {"user_id":session["user_id"]})
    return result.fetchall()

def send(date, title, description, id, user_id, report_type):
    sql = "INSERT INTO reports (date, title, description, location_id, user_id, report_type, created_at) VALUES \
        (:date, :title, :description, :location, :user_id, :report_type, date_trunc('minute', CURRENT_TIMESTAMP))"
    db.session.execute(
    sql, {"date":date, "title":title, "description":description, "location":id, "user_id":user_id, "report_type":report_type})
    db.session.commit()
        
def get_report(id):
    sql = "SELECT A.id, title, date, B.location_name, description, \
        location_name, C.type FROM reports A, locations B, report_types C WHERE \
        A.id=:id AND A.location_id = B.id AND A.report_type = C.id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def get_report_types():
    sql = "SELECT id, type FROM report_types"
    result = db.session.execute(sql)
    return result
    
def delete(id):
    sql = "DELETE FROM reports WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()