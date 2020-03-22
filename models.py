import datetime
from app import db

class Location(db.Model):
    __tablename__ = 'covid19'

    name = db.Column(db.String(),primary_key = True)
    latitude = db.Column(db.Float,default = 0.0)
    longitude = db.Column(db.Float,default = 0.0)
    situation = db.Column(db.PickleType())
    def __init__(self,name,location):
        self.name = name
        self.latitude = location[0]
        self.longitude = location[1]
        self.situation = [(0,0)]
    def __repr__(self):
        return '<id {}>'.format(self.id)
