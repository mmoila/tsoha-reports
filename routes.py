from werkzeug.utils import redirect
from app import app
from flask import render_template, request
from reports import Report
from db import db

@app.route("/")
def index():
    title = "test"
    return render_template("index.html")

@app.route("/new")
def new():
    result = db.session.execute("SELECT id, \
        (CONCAT(location_name, ' (', IATA_ident, ')')) AS location FROM locations")
    locations = result.fetchall()
    return render_template("new.html", locations=locations)

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
   