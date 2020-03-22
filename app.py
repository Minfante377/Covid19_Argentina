from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_googlemaps import GoogleMaps
import os
from utils import update_markers,update_status_provincias,update_status_pais
from datetime import date

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
GoogleMaps(app)
from models import Location


@app.route('/',methods=['GET', 'POST'])
def index():
    status = update_status_provincias()
    pais = update_status_pais()
    for s in status:
        today = date.today()
        location = db.session.query(Location).filter_by(name = s[0]).first()
        try:
            location.situation = [today,s[1],s[2]]
        except:
            print("No se encuentra " +s[0]+" en la base de datos")
            continue
        print(location.name)
        db.session.commit() 
    locations = db.session.query(Location).all()
    markers = update_markers(locations)
    return render_template('index.html',location=locations, markers=markers)

if __name__ == '__main__':
    app.run()
