from flask import abort, session

LIMITS = {
    "title": 50, "description": 1000, "loc_name": 50, "username": 30,
    "password": 30
    }
EXACT_LIMITS = {"icao": 4, "iata": 3}


def check_csrf(form_token):
    if session["csrf_token"] != form_token:
        return abort(403)

def is_valid(fields):
    for key in fields:
        value = fields[key]
        if len(value) == 0:
            return "You must fill in all the fields."
        elif key in LIMITS and len(value) > LIMITS[key]:
            return f"{key} must be under {LIMITS[key]} characters long."
        elif key in EXACT_LIMITS and len(value) != EXACT_LIMITS[key]:
            return f"{key} must be {EXACT_LIMITS[key]} characters long."
    return True