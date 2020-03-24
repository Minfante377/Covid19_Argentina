from flask import Flask,render_template,Response
from flask_sqlalchemy import SQLAlchemy
from flask_googlemaps import GoogleMaps
import os
import io
from utils import update_markers,update_status_provincias,update_status_pais,create_figure_dot,create_figure_bar
from datetime import date
from bokeh.embed import components

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
GoogleMaps(app)
from models import Location
from utils import create_figure_dot

@app.route('/',methods=['GET', 'POST'])
def index():
    status = update_status_provincias()
    pais = update_status_pais()
    for s in status:
        location = db.session.query(Location).filter_by(name = s[0]).first()
        try:
            location.situation = [s[1],s[2]]
        except:
            print("No se encuentra " +s[0]+" en la base de datos")
            continue
        db.session.commit() 
    locations = db.session.query(Location).all()
    markers = update_markers(locations)
    plot_dot = create_figure_dot(pais)
    script_dot,div_dot = components(plot_dot)
    plot_bar = create_figure_bar(pais)
    script_bar,div_bar = components(plot_bar)
    return render_template('index.html',location=locations, markers=markers,script_dot = script_dot,div_dot = div_dot,script_bar = script_bar,div_bar = div_bar)

if __name__ == '__main__':
    app.run()
