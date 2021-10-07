from db import db

def get_all():
    sql = "SELECT A.message, B.username, A.created_at, A.id FROM message_board A, \
        users B WHERE A.user_id = B.id"
    result = db.session.execute(sql)
    return result.fetchall()

def delete(id):
    sql = "DELETE FROM message_board WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    
def create(message_content, id):
    sql = "INSERT INTO message_board \
        (message, user_id, created_at) VALUES \
        (:message_content, :id, date_trunc('minute', CURRENT_TIMESTAMP))"
    db.session.execute(sql, {"message_content":message_content, "id":id})
    db.session.commit()