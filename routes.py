from werkzeug.utils import redirect
from app import app
from flask import render_template, request, session, flash
from db import db
import users
import reports
import secrets
import locations
import messages
import validations

@app.route("/")
def index():
    if users.count_admins() == 0:
        session["no_admins"] = True
        session["csrf_token"] = secrets.token_hex(16)
        return render_template("index.html")
    notes = messages.get_all()
    return render_template("index.html", notes=notes)

@app.route("/login",methods=["POST"])
def login():
    session["csrf_token"] = secrets.token_hex(16)
    username = request.form["username"]
    password = request.form["password"]
    if users.check_login(username, password):
        session["username"] = username
        session["admin"] = False
        if users.is_admin(session["user_id"]):
            session["admin"] = True
    return redirect("/")
    
@app.route("/logout")
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect("/")

@app.route("/new")
def new():
    ad_list = locations.get_summary_list()
    report_types = reports.get_report_types()
    return render_template("new-report.html", locations=ad_list, report_types=report_types)

@app.route("/send", methods=["POST"])
def send():
    validations.check_csrf(session["csrf_token"])
    fields = request.form
    validation_result = validations.is_valid(fields)
    if validation_result == True:
        date = fields["date"]
        title = fields["title"]
        description = fields["description"]
        location_id = fields["location"]
        report_type = fields["report_type"]
        reports.send(date, title, description, location_id, session["user_id"], report_type)
    else:
        flash(validation_result, "warning")
        return redirect("/new")
    flash("Report sent successfully", "info")
    return redirect("/")
    

@app.route("/result")
def result():
    try:
        args = request.args
        result = reports.get_filtered(args)
        return render_template("result.html", reports=result)
    except:
        result = reports.get_all()
        return render_template("result.html", reports=result)
    
@app.route("/user", methods=["GET", "POST"])
def user():
    if session["admin"]:
        if request.method == "GET":
            return render_template("new-user.html")
        if request.method == "POST":
            validations.check_csrf(session["csrf_token"])
            fields = request.form
            validation_result = validations.is_valid(fields)
            if validation_result != True:
                flash(validation_result, "warning")
                return redirect("/user")
            try:
                admin = request.form["admin"]
                users.create_user(fields["username"], fields["password"], admin)
            except:
                users.create_user(fields["username"], fields["password"])
            flash("New user created.", "info")
            return redirect("/")
    return redirect("/")

@app.route("/user-init", methods=["GET", "POST"])
def user_init():
    if request.method == "GET":
        return render_template("user-init.html")
    validations.check_csrf(session["csrf_token"])
    fields = request.form
    validation_result = validations.is_valid(fields)
    if validation_result != True:
        flash(validation_result, "warning")
    admin = "1"
    users.create_user(fields["username"], fields["password"], admin)
    del session["no_admins"]
    return redirect("/")

@app.route("/report/<int:id>")
def report(id):
    if session["admin"]:
        report = reports.get_report(id)
        return render_template("report.html", report=report)
    return redirect("/")

@app.route("/report/delete/<int:id>", methods=["POST"])
def delete(id):
    validations.check_csrf(session["csrf_token"])
    if session["admin"]:
        reports.delete(id)
        return redirect("/result")
    return redirect("/")

@app.route("/user/search")
def user_search():
    if session["admin"]:
        user_list = users.get_all()
        return render_template("users.html", user_list=user_list)
    return redirect("/")

@app.route("/change-state/<int:id>", methods=["POST"])
def change_state(id):
    validations.check_csrf(session["csrf_token"])
    if session["admin"]:
        if users.change_state(id):
            return redirect("/user/search")
        flash("Can't deactivate last user/admin.", "warning")
    return redirect("/")

@app.route("/change-rights/<int:id>", methods=["POST"])
def change_rights(id):
    validations.check_csrf(session["csrf_token"])
    if session["admin"]:
        if users.change_rights(id):
            return redirect("/user/search")
        flash("Can't deactivate last admin.", "warning")
    return redirect("/")

@app.route("/change-password", methods=["GET", "POST"])
def change_password():
    if request.method == "GET":
        return render_template("change-password.html")
    if request.method == "POST":
        validations.check_csrf(session["csrf_token"])
        fields = request.form
        validation_result = validations.is_valid(fields)
        if validation_result != True:
            flash(validation_result, "warning")
        password = fields["password"]
        c_password = fields["cPassword"]
        if password == c_password:
            users.change_password(session["user_id"], password)
            flash("Password changed successfully!", "info")
            return redirect("/")
        else:
            flash("Passwords didn't match.", "warning")
            return redirect("/change-password")

@app.route("/aerodromes")
def aerodromes():
    if session["admin"]:
        ad_list = locations.get_all()
        return render_template("locations.html", aerodromes=ad_list)
    return render_template("/error.html", error="You must have admin rights to manage aerodromes!")

@app.route("/aerodromes/add", methods=["POST"])
def add_aerodrome():
    validations.check_csrf(session["csrf_token"])
    if session["admin"]:
        fields = request.form
        validation_result = validations.is_valid(fields)
        if validation_result != True:
            flash(validation_result, "warning")
        if locations.add(fields["icao"], fields["iata"], fields["loc_name"]):
            return aerodromes()
    flash("Location already exists.", "warning")
    return redirect("/aerodromes")

@app.route("/delete-message", methods=["POST"])
def delete_message():
    validations.check_csrf(session["csrf_token"])
    message_id = request.form["message_id"]
    messages.delete(message_id)
    return redirect("/")
    
@app.route("/create-message", methods=["POST"])
def create_message():
    validations.check_csrf(session["csrf_token"])
    fields = request.form
    validation_result = validations.is_valid(fields)
    if validation_result == True:
        messages.create(fields["message-content"], session["user_id"])
    else:
        flash("Cannot create blank message", "warning")
    return redirect("/")