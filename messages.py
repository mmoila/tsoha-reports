from db import db

def get_all():
    sql = "SELECT A.message, B.username, A.created_at FROM message_board A, \
        users B WHERE A.user_id = B.id"
    result = db.session.execute(sql)
    return result.fetchall()

def delete(id):
    sql = "DELETE FROM reports WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    