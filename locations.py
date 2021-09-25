from db import db

def get_summary_list():
    result = db.session.execute("SELECT id, \
        (CONCAT(location_name, '(', IATA_ident, ')')) AS location FROM locations")
    return result.fetchall()

def get_all():
    result = db.session.execute("SELECT ICAO_ident, IATA_ident, location_name FROM locations")
    return result.fetchall()

def add(icao, iata, name):
    try:
        sql = "INSERT INTO locations (ICAO_ident, IATA_ident, location_name) \
                VALUES (:icao, :iata, :name)" 
        db.session.execute(sql, {"icao":icao, "iata":iata, "name":name})
        db.session.commit()
        return True
    except:
        return False

def delete():
    pass