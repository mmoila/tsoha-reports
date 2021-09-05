from db import db

class Reports():

    def get_all(self):
        sql = "SELECT * FROM reports"
        result = db.session.execute(sql)
        return result.fetchall()


class Report():
    def __init__(self, title=None, description=None, location=None):
        self.__title = title
        self.__description = description
        self.__location = location
        
    def get_title(self):
        return self.__title

    def get_description(self):
        return self.__description

    def get_location(self):
        return self.__location

    def set_title(self, title):
        self.__title = title

    def set_description(self, description):
        self.__description = description

    def set_location(self, location):
        self.__location = location

    def send(self):
        sql = "INSERT INTO reports (title, description, location_id) VALUES \
            (:title, :description, :location)"
        db.session.execute(
            sql, {"title":self.__title,
            "description":self.__description, "location":self.__location})
        db.session.commit()
        

    