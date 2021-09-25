from logging import error
from werkzeug.utils import redirect
from app import app
from flask import render_template, request, session, abort
from db import db
import users
import reports
import secrets
import locations

@app.route("/")
def index():
    title = "test"
    if users.count_admins() == 0:
        session["no_admins"] = True
        return render_template("new-user.html")
    return render_template("index.html", title=title)

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
    else:
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
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    date = request.form["date"]
    title = request.form["title"]
    if len(title) > 50:
        return render_template("error.html", error = "Title is too long!")
    description = request.form["description"]
    if len(description) > 1000:
        return render_template("error.html", error="Max description length is 1000 characters")
    location_id = request.form["location"]
    report_type = request.form["report_type"]
    reports.send(date, title, description, location_id, session["user_id"], report_type)
    return redirect("/")

@app.route("/result")
def result():
    try:
        args = request.args
        if args["location"] == "" and args["title"] == "":
            result = reports.get_all()
        else:
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
            if session["csrf_token"] != request.form["csrf_token"]:
                return abort(403)
            username = request.form["username"]
            password = request.form["password"]
            if len(username) > 30 or len(password) > 30:
                return render_template("error.html", error="Username or password is too long!")
            try:
                admin = request.form["admin"]
                users.create_user(username, password, admin)
            except:
                users.create_user(username, password)
            return redirect("/")
    return redirect("/")

@app.route("/user-init", methods=["GET", "POST"])
def user_init():
    if request.method == "GET":
            session["csrf_token"] = secrets.token_hex(16)
            return render_template("new-user.html")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        username = request.form["username"]
        password = request.form["password"]
        if len(username) > 30 or len(password) > 30:
            return render_template("error.html", error="Username or password is too long!")
        admin = "1"
        users.create_user(username, password, admin)
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
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
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
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if session["admin"]:
        if users.change_state(id):
            return redirect("/user/search")
        return render_template("error.html", error="Can't deactivate last user/admin...")
    return redirect("/")

@app.route("/change-rights/<int:id>", methods=["POST"])
def change_rights(id):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    if session["admin"]:
        if users.change_rights(id):
            return redirect("/user/search")
        return render_template("error.html", error="Can't deactivate last admin")
    return redirect("/")

@app.route("/change-password", methods=["GET", "POST"])
def change_password():
    if request.method == "GET":
        return render_template("change-password.html")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        password = request.form["password"]
        c_password = request.form["cPassword"]
        if password == c_password:
            users.change_password(session["user_id"], password)
            return redirect("/")
        else:
            return render_template("error.html", error="Passwords didn't match")

@app.route("/aerodromes")
def aerodromes():
    if session["admin"]:
        ad_list = locations.get_all()
        return render_template("locations.html", aerodromes=ad_list)
    return render_template("/error.html", error="You must have admin rights to manage aerodromes!")

@app.route("/aerodromes/add", methods=["POST"])
def add_aerodrome():
    print("degdgs")
    if session["csrf_token"] != request.form["csrf_token"]:
        print("debug")
        abort(403)
    if session["admin"]:
        print("debug2")
        icao = request.form["icao"]
        if len(icao) != 4:
            return render_template("error.html",
             error="ICAO identification must be four characters long!")
        iata = request.form["iata"]
        if len(iata) != 3:
            return render_template("error.html",
             error="IATA identification must be three characters long!")
        loc_name = request.form["loc_name"]
        if len(loc_name) > 50:
            return render_template("error.html",
             error="Max location name length is 50 characters")
        if locations.add(icao, iata, loc_name):
            return aerodromes()
    return render_template("error.html", error="Location already exists!")
    
