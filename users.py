from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session

def create_user(username, password):
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password, is_admin) \
        VALUES (:username, :password, :is_admin)"
    db.session.execute(sql, {"username":username, "password":hash_value, "is_admin":'0'})
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
