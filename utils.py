from flask_googlemaps import icons
import requests
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib.figure import Figure
from matplotlib import dates
from matplotlib.ticker import MultipleLocator
import datetime
import numpy as np

URL = 'https://es.wikipedia.org/wiki/Pandemia_de_enfermedad_por_coronavirus_de_2020_en_Argentina'

def update_markers(location):
    markers = []
    for l in location:
        m = {'icon':icons.alpha.B,'lat':l.latitude,'lng':l.longitude,'infobox':l.name+'\n'+"Casos confirmados:"+str(l.situation[1])+"\n"+"Muertes:"+str(l.situation[2])}
        markers.append(m)
    return markers

def update_status_provincias():
    status = []
    response = requests.get(URL).text
    soup = BeautifulSoup(response,'lxml')
    table = soup.find('table',{'class':'wikitable sortable col2der col3der col4der col5der col6der'})
    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        if not tds:
            continue
        provincia,casos,poblacion,prevalencia,muertes,recuperaciones = [td.text.strip() for td in tds[:6]]
        if '!' in provincia:
            provincia = provincia[provincia.index('!')+1:]
        provincia = provincia.replace("Provincia de ","")
        estado_actual = (provincia,casos,muertes)
        status.append(estado_actual)
    return status

def update_status_pais():

    response = requests.get(URL).text
    soup = BeautifulSoup(response,'lxml')
    table = soup.find('table',{'style':'text-align:left; border-collapse:collapse; width:100%;'})
    tbody = table.find('tbody')
    casos = None
    fechas = None
    pais = []
    for tr in tbody('tr'):
        td = tr.find("td",{'style':'padding-left:0.4em; padding-right:0.4em; text-align:center'})
        if td:
            fechas = td.text
        for td in tr.find_all("td"):
            span = td.find("span",{'style':'width: 3.5em;padding:0 0.3em 0 0; text-align:right; display: inline-block;'})
            if span:
                casos = span.text
        pais.append((fechas,casos))
    print (pais)
    return pais

def create_figure(pais):
    fig = Figure()
    fig.set_figheight(10)
    fig.set_figwidth(10)
    axis = fig.add_subplot(2,1,1)
    xs = []
    ys = []
    for day in pais:
        if not day[0] or day[0] == "⋮":
            continue
        fecha = datetime.datetime.strptime(day[0],'%d-%m-%Y')
        casos = day[1]
        xs.append(fecha)
        ys.append(int(casos))
    xs = dates.date2num(xs)
    hfmt = dates.DateFormatter('%d\n%m')
    axis.xaxis.set_major_formatter(hfmt)
    axis.tick_params(axis='both',labelsize='10')
    axis.set_xticks(xs)
    ys_ticks = [y for y in ys if y > 0]
    axis.set_yticks(ys_ticks)
    axis.grid()
    axis.yaxis.set_major_locator(MultipleLocator(10.0))
    axis.title.set_text("Evolucion del total de casos")
    axis.stem(xs,ys,label = "Casos totales por dia")
    axis = fig.add_subplot(2,1,2)
    ys_porcentual = []
    ys_porcentual.append(0.00)
    for i in range(1,len(ys)):
        ys_porcentual.append((ys[i]-ys[i-1])/ys[i-1]*100)
    ys_ticks = [y for y in ys if y < 100]
    axis.xaxis.set_major_formatter(hfmt)
    axis.tick_params(axis='both',labelsize='10')
    axis.set_xticks(xs)
    axis.set_yticks(ys_ticks)
    axis.grid(axis = "y")
    axis.yaxis.set_major_locator(MultipleLocator(25.0))
    axis.title.set_text("Aumento porcentual de casos respecto al dia anterior")
    axis.bar(xs,ys_porcentual)
    return fig

