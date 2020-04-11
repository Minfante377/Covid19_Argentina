import requests
from bs4 import BeautifulSoup
import datetime
from bokeh.plotting import figure
import folium
from init_db import init_db

URL = 'https://es.wikipedia.org/wiki/Pandemia_de_enfermedad_por_coronavirus_de_2020_en_Argentina'
start_coords = (-50.7462676,-63.6999338)
start_zoom = 4.2

def update_markers(location):
    markers = []
    for l in location:
        print(l)
        m = {'lat':l[1][0],'lng':l[1][1],'infobox':l[0]+" - Casos confirmados:"+str(l[2][0])+" - Muertes:"+str(l[2][1])}
        markers.append(m)
    return markers

def update_status_provincias():
    status = []
    response = requests.get(URL).text
    soup = BeautifulSoup(response,'lxml')
    table = soup.find('table',{'class':'wikitable sortable col2der col3der col4der col5der col6der col7der'})
    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        if not tds:
            continue
        provincia,casos,poblacion,prevalencia,muertes,recuperaciones = [td.text.strip() for td in tds[:6]]
        if '!' in provincia:
            provincia = provincia[provincia.index('!')+1:]
        provincia = provincia.replace("Provincia de ","")
        provincia = provincia.replace("Provincia del ","")
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

def create_figure_dot(pais):
    xs = []
    ys = []
    for day in pais:
        if not day[0] or day[0] == "⋮":
            continue
        fecha = datetime.datetime.strptime(day[0],'%d-%m-%Y')
        casos = day[1]
        xs.append(fecha)
        ys.append(int(casos))
    p = figure(sizing_mode = "scale_both",x_axis_type='datetime',title = "Evolucion del total de casos",width = 600,height = 450)
    p.axis.axis_label = 'Fecha'
    p.yaxis.axis_label = 'Numero de casos'
    p.circle(xs,ys,size = 5, color = 'navy')
    return p

def create_figure_bar(pais):
    xs = []
    ys = []
    for day in pais:
        if not day[0] or day[0] == "⋮":
            continue
        fecha = datetime.datetime.strptime(day[0],'%d-%m-%Y')
        casos = day[1]
        xs.append(fecha)
        ys.append(int(casos))
    ys_porcentual = []
    ys_porcentual.append(0.00)
    for i in range(1,len(ys)):
        ys_porcentual.append((ys[i]-ys[i-1])/ys[i-1]*100)
    p = figure(sizing_mode = 'scale_both',x_axis_type='datetime',y_axis_type = 'linear',title = "Aumento porcentual respecto al dia anterior",width = 600,height = 450)
    p.axis.axis_label = 'Fecha'
    p.yaxis.axis_label = '%'
    p.vbar(x = xs,top = ys_porcentual,width = 0.8,line_width = 10, fill_color = 'navy')
    p.y_range.start = 0
    return p

def create_map():
    status = update_status_provincias()
    locations = init_db()
    for s in status:
        for location in locations:
            if s[0] == location[0]:
                try:
                    location[2] = (s[1],s[2])
                except:
                    print("No se encuentra " +s[0]+" en la base de datos")
                    continue
    markers = update_markers(locations)
    folium_map = folium.Map(location=start_coords,zoom_start = start_zoom)
    for marker in markers:
        popup = folium.Popup(marker['infobox'],max_width = 500)
        folium.Marker((marker['lat'],marker['lng']),popup = popup).add_to(folium_map)
    return folium_map
