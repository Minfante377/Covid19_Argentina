from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
import matplotlib.pyplot as plt
import matplotlib
from functools import partial
from datetime import datetime
import requests
import json
import numpy as np

url = "http://127.0.0.1:5000/refresh"

class Covid(App):

    def build(self):
        self.refresh()
        self.refresh_dropdown()
        root = FloatLayout()
        self.layout = BoxLayout(orientation="vertical")
        self.title_box = BoxLayout(orientation = "horizontal",spacing = 20)
        self.header = Label(text ='[u][b]Argentina COVID-19[/b][/u]',font_size = 30,markup = True)
        self.title_box.add_widget(self.header)
        self.layout.add_widget(self.title_box)
        self.graficas_box = BoxLayout(orientation="horizontal")
        self.pais_box = BoxLayout(orientation="vertical")
        self.pais_label = Label(text = "Evolucion de casos confirmados")
        self.draw_graph()
        self.pais_box.add_widget(self.pais_label)
        self.pais_box.add_widget(self.casos_graph)
        self.graficas_box.add_widget(self.pais_box)
        self.provincias_box = BoxLayout(orientation="vertical")
        mainbutton = Button(text="Provincias...")
        mainbutton.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x:setattr(mainbutton,'text',x))
        self.dropdown.bind(on_select=lambda instance,x:self.update_labels(x))
        self.provincias_box.add_widget(mainbutton)
        self.provincias_box.add_widget(self.casos_label)
        self.provincias_box.add_widget(self.muertes_label)
        self.graficas_box.add_widget(self.provincias_box)
        #self.dropdown.bind(on_select = refresh_provincias())
        self.layout.add_widget(self.graficas_box)
        self.refresh_box = BoxLayout(orientation="horizontal")
        self.refresh_button = Button(text="Actualizar")
        self.last_update = Label(text = "Ultima actualizacion:")
        self.refresh_button.bind(on_press=partial(self.refresh_on_click,self.refresh_button))
        self.refresh_box.add_widget(self.last_update)
        self.refresh_box.add_widget(self.refresh_button)
        self.layout.add_widget(self.refresh_box) 
        root.add_widget(self.layout)
        return root

    def update_labels(self,name):
        for provincia in self.provincias:
            if provincia[0] == name:
                self.casos_label.text = "Casos confirmados: "+str(provincia[2][0])
                self.muertes_label.text = "Muertes: "+str(provincia[2][1])

    def draw_graph(self):
        xs = []
        ys = []
        for p in self.pais:
            if p[0] == None or p[0] == "⋮":
                continue
            xs.append(datetime.strptime(p[0],"%d-%m-%Y"))
            ys.append(int(p[1]))
        xs = matplotlib.dates.date2num(xs)
        hftm = matplotlib.dates.DateFormatter("%d-%m-%Y")
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.xaxis.set_major_formatter(hftm)
        plt.setp(ax.get_xticklabels(),rotation = 15)
        ax.stem(xs,ys)
        ax.set_xticks(xs)
        ax.set_yticks(np.arange(0,max(ys),50))
        plt.grid()
        self.casos_graph = FigureCanvasKivyAgg(plt.gcf())

    def refresh_dropdown(self):
        self.casos_label = Label(text="Casos confirmados:")
        self.muertes_label = Label(text="Muertes:")
        self.dropdown = DropDown()
        for i in range (len(self.provincias)):
            btn = Button(text = str(self.provincias[i][0]),height=30,size_hint_y=None)
            btn.bind(on_release=lambda btn:self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
     
    def refresh(self):
        response = requests.get(url)
        response = json.loads(response.text)
        self.pais = response["pais"]
        self.provincias = response["provincias"] 

    def refresh_on_click(self,instance,*args):
        ts = datetime.now() 
        self.last_update.text = "Ultima actualizacion: "+str(ts)[:-10]
        self.refresh()
        self.draw_graph()

Covid().run()
