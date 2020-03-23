#Este repositorio ha sido creado exclusivamente para uso personal.

Este repositorio implementa una aplicacion web basica para visualizar el avance de la epidemia COVID-19 en Argentina. Permite la visualizacaion de los casos confirmados y muertes por provincias, utilizando un mapa interactivo. A su vez, muestra graficas del avance de los casos confirmados por dia en todo el pais, y el aumento porcentual de los mismos respecto al dia anterior.
Toda la informacion se toma automaticamente de https://es.wikipedia.org/wiki/Pandemia_de_enfermedad_por_coronavirus_de_2020_en_Argentina.
#Requerimientos
 La lista de modulos requeridos se encuentra en requirements.txt:
#Uso
- Debe crearse una base de datos con una tabla llamada covid19
- Correr el script init_db.py:

	python3 init_db.py
	
  El mismo creara todas las provincias con sus marcadores para ubicar en el mapa
- Correr la aplicacion web:

	python3 manage.py runserver
	
  La misma podra visualizarse en http://127.0.0.1:5000/
