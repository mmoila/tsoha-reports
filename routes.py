from werkzeug.utils import redirect
from app import app
from flask import render_template, request, session
from reports import Report
from db import db
from users import check_login, create_user

@app.route("/")
def index():
    title = "test"
    return render_template("index.html", title=title)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if check_login(username, password):
        session["username"] = username
        return redirect("/")
    else:
        return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
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
    description = request.form["description"]
    location_id = request.form["location"]
    report = Report(title, description, location_id)
    report.send()
    return redirect("/")

@app.route("/result")
def result():
    result = db.session.execute("SELECT * FROM reports")
    reports = result.fetchall()
    return render_template("result.html", reports=reports)

@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == "GET":
        return render_template("new-user.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        create_user(username, password)
        return redirect("/")