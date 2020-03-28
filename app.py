from flask import Flask,render_template,Response
import os
import io
from datetime import date
from bokeh.embed import components

app = Flask(__name__)
APP_SETTINGS="config.DevelopmentConfig"
app.config.from_object(APP_SETTINGS)

from utils import update_markers,create_map,update_status_pais,create_figure_dot,create_figure_bar

@app.route('/',methods=['GET', 'POST'])
def index():
    pais = update_status_pais()
    plot_dot = create_figure_dot(pais)
    script_dot,div_dot = components(plot_dot)
    plot_bar = create_figure_bar(pais)
    script_bar,div_bar = components(plot_bar)
    f_map = create_map()
    f_map.save('templates/map.html')
    return render_template('index.html',script_dot = script_dot,div_dot = div_dot,script_bar = script_bar,div_bar = div_bar)

if __name__ == '__main__':
    app.run()
