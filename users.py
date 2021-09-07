from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session

def create_user(username, password, admin = "0"):
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password, is_admin) \
        VALUES (:username, :password, :is_admin)"
    db.session.execute(sql, {"username":username, "password":hash_value, "is_admin":admin})
    db.session.commit()

def check_login(username, password):
    sql = "SELECT id, password, is_admin FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        else:
            return False

def is_admin():
    sql = "SELECT 1 FROM users WHERE is_admin='1' and id=:user_id"
    result = db.session.execute(sql, {"user_id":session["user_id"]})
    admin = result.fetchone()
    if not admin:
        return False
    return True

def no_admins():
    sql = "SELECT 1 FROM users WHERE is_admin='1'"
    result = db.session.execute(sql)
    admin = result.fetchone()
    if not admin:
        return True
    return False