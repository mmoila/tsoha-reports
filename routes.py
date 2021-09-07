from werkzeug.utils import redirect
from app import app
from flask import render_template, request, session
from reports import Report
from db import db
from users import check_login, create_user, is_admin, no_admins

@app.route("/")
def index():
    title = "test"
    if no_admins():
        session["no_admins"] = True
        return render_template("new-user.html")
    return render_template("index.html", title=title)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if check_login(username, password):
        session["username"] = username
        session["admin"] = False
        if is_admin():
            session["admin"] = True
        return redirect("/")
    else:
        return redirect("/")

@app.route("/logout")
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect("/")

@app.route("/new")
def new():
    result = db.session.execute("SELECT id, \
        (CONCAT(location_name, ' (', IATA_ident, ')')) AS location FROM locations")
    locations = result.fetchall()
    return render_template("new-report.html", locations=locations)

@app.route("/send", methods=["POST"])
def send():
    title = request.form["title"]
    if len(title) > 50:
        return render_template("error.html", error = "Title is too long!")
    description = request.form["description"]
    if len(description) > 1000:
        return render_template("error.html", error="Max description length is 1000 characters")
    location_id = request.form["location"]
    report = Report(title, description, location_id)
    report.send()
    return redirect("/")

@app.route("/result")
def result():
    if session["admin"]:
        result = db.session.execute("SELECT * FROM reports")
        reports = result.fetchall()
        return render_template("result.html", reports=reports)
    return redirect("/")

@app.route("/user", methods=["GET", "POST"])
def user():
    if session["admin"]:
        if request.method == "GET":
            return render_template("new-user.html")
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            if len(username) > 30 or len(password) > 30:
                return render_template("error.html", error="Username or password is too long!")
            try:
                admin = request.form["admin"]
                create_user(username, password, admin)
            except:
                create_user(username, password)
            return redirect("/")
    return redirect("/")

@app.route("/user-init", methods=["GET", "POST"])
def user_init():
    if request.method == "GET":
            return render_template("new-user.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if len(username) > 30 or len(password) > 30:
            return render_template("error.html", error="Username or password is too long!")
        admin = "1"
        create_user(username, password, admin)
        del session["no_admins"]
        return redirect("/")