from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session

def create_user(username, password, admin = "0"):
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password, is_admin, is_active) \
        VALUES (:username, :password, :is_admin, '1')"
    db.session.execute(sql, {"username":username, "password":hash_value, "is_admin":admin})
    db.session.commit()

def check_login(username, password):
    sql = "SELECT id, password, is_admin FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    elif is_active(user.id):
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        else:
            return False

def is_admin(user_id):
    sql = "SELECT 1 FROM users WHERE is_admin='1' and id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    admin = result.fetchone()
    if not admin:
        return False
    return True

def count_admins():
    sql = "SELECT COUNT(*) FROM users WHERE is_admin='1'"
    result = db.session.execute(sql)
    count = result.fetchone()[0]
    return count

def is_active(id):
    sql = "SELECT 1 FROM users WHERE is_active='1' and id=:id"
    result = db.session.execute(sql, {"id":id})
    if result.fetchone():
        return True
    return False
    
def get_all():
    sql = "SELECT id, username, is_admin, is_active FROM USERS ORDER BY id"
    result = db.session.execute(sql)
    return result.fetchall()

def change_state(id):
    sql = "SELECT COUNT(*) FROM users WHERE is_active = '1'" 
    result = db.session.execute(sql)
    active_users = result.fetchone()[0]
    if active_users == 1 and is_active(id):
        return False
    if count_admins() > 1 or not is_admin(id):
        sql = "UPDATE users SET is_active = NOT is_active WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    else:
        return False
    
    