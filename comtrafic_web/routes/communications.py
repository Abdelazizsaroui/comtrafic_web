# Le backend de la page Communications
# La page Communications existe sur l'interface en 3 versions
# connectées à l'API en JSON, XML et CSV

import requests, datetime
import csv, io
import xml.etree.ElementTree as ET
from flask import render_template, jsonify, request
from comtrafic_web import app
from comtrafic_web.routes import api_url, periode, etat_api


# Ces données Postes et Services sont utilisées
# uniquement pour leurs listes dérolantes
# corréspondates dans le forumulaire de filtrage
# sur la page Communications
# Pour regénérer ces données, exécutez les scripts
# sur le répértoire ./scripts
postes = {'921', '935', '904', '902', '929', '949', '930', '932', '944', '900', '525', '928', '937', '933', '910', '931', '905', '907', '901', '934', '948', '938', '917', '922', '916', '912', '909', '903'}
services = {'Informatique', 'Support technique', 'Direction', 'Expéditions Stock', 'Technique', 'Achats Approvisionnements', 'Service_Defaut', 'Chambres', 'Compta', 'Commercial'}

# Cette fonction serve la page statique «communications.html»
@app.route("/communications")
def communications():
	return render_template("communications.html", etat_api=etat_api(), postes=postes, services=services)

# Cette fonction serve la page statique «communications_xml.html»
@app.route("/communications/_xml_")
def communications_xml():
	return render_template("communications_xml.html", etat_api=etat_api(), postes=postes, services=services)

# Cette fonction serve la page statique «communications_csv.html»
@app.route("/communications/_csv_")
def communications_csv():
	return render_template("communications_csv.html", etat_api=etat_api(), postes=postes, services=services)

# Cette fonction fournit les données des communications de l'API
# suite à une requête AJAX de la page «communications.html»
@app.route("/com-data")
def com_data():
	# On teste si la requête vient avec des arguments (filtres de recherche)
	# La requête vient avec 0 arguments dans 2 cas:
	# 1 - Lorsque la page se charge
	# 2 - Lorsque on clique sur «Recherche» sans avoir ajouté de filtres 
	if len(request.args) > 0:
		# Si on a des arguments, on les joint avec la requête envoyée à l'API
		# La réponse retournée par défaut est en JSON
		search_query = ""
		for el in request.args:
			search_query += el + "=" + request.args.get(el) + "&"
		raw_res = requests.get(f"{api_url}ED&CO_DATE={periode}&{search_query}")
	else:
		# Sinon on envoie la requête à l'API sans arguments de recherche
		raw_res = requests.get(f"{api_url}ED&CO_DATE={periode}")
	# On extrait le contenu JSON de la réponse de l'API
	res = raw_res.json()
	# Puis on retient juste la section «Data» du JSON, qui contient les
	# enregistrements des communications
	data = res['Data']
	if data == "":
		# Si data est vide est n'est pas une liste, ceci lorsque la réponse
		# ne contient aucun élément, on le convertit en liste pour retourner
		# une réponse JSON valide
		data = []
	else:
		# Pour chaque enregitrement de communication, on convertit les durées
		# en secondes au format HH:MM:SS
		for el in data:
			el['CO_DUR'] = str(datetime.timedelta(seconds = el['CO_DUR']))
			el['CO_DRING'] = str(datetime.timedelta(seconds = el['CO_DRING']))
			el['CO_DRTOT'] = str(datetime.timedelta(seconds = el['CO_DRTOT']))
	# On retourne les données des communications en JSON à l'interface
	return jsonify(data)

# Cette fonction fournit les données des communications de l'API
# suite à une requête AJAX de la page «communications_xml.html»
@app.route("/com-data-xml")
def com_data_xml():
	# On teste si la requête vient avec des arguments (filtres de recherche)
	# La requête vient avec 0 arguments dans 2 cas:
	# 1 - Lorsque la page se charge
	# 2 - Lorsque on clique sur «Recherche» sans avoir ajouté de filtres
	if len(request.args) > 0:
		# Si on a des arguments, on les joint avec la requête envoyée à l'API
		# On spécifie qu'on veut les données en format XML avec -format=XML
		search_query = ""
		for el in request.args:
			search_query += el + "=" + request.args.get(el) + "&"
		raw_res = requests.get(f"{api_url}ED&CO_DATE={periode}&{search_query}&-format=XML")
	else:
		# Sinon on envoie la requête à l'API sans arguments de recherche
		raw_res = requests.get(f"{api_url}ED&CO_DATE={periode}&-format=XML")
	# On charge le contenu XML de la réponse sur xml_root
	xml_root = ET.fromstring(raw_res.content)
	# Puis on extrait le nombre des lignes des communications
	# xml_root[0][3] retourne la ligne où se trouve l'information
	# de nombre des lignes, puis on extrait son text avec text[2:-1]
	# on peut faire juste xml[0][3].text mais en va avoir une erreur
	# lorsque on va convertir en entier car ça retourne des "" avec
	# les chiffres
	lines = xml_root[0][3].text[2:-1]
	n = int(lines)
	# On initialise la réponse qui va être retournée
	data = []
	# On joint chaque ligne de communication à la réponse
	# xml[2][i].attrib retourne un dictionnaire avec les noms 
	# et les valeurs de chaque champ comme en JSON
	for i in range(n):
		data.append(xml_root[2][i].attrib)
	else:
		for el in data:
			# Pour chaque enregitrement de communication, on convertit les durées
			# en secondes au format HH:MM:SS
			el['CO_DUR'] = str(datetime.timedelta(seconds = int(el['CO_DUR'])))
			el['CO_DRING'] = str(datetime.timedelta(seconds = int(el['CO_DRING'])))
			el['CO_DRTOT'] = str(datetime.timedelta(seconds = int(el['CO_DRTOT'])))
	# On retourne les données des communications en JSON à l'interface
	return jsonify(data)

# Cette fonction fournit les données des communications de l'API
# suite à une requête AJAX de la page «communications_csv.html»
@app.route("/com-data-csv")
def com_data_csv():
	# On teste si la requête vient avec des arguments (filtres de recherche)
	# La requête vient avec 0 arguments dans 2 cas:
	# 1 - Lorsque la page se charge
	# 2 - Lorsque on clique sur «Recherche» sans avoir ajouté de filtres
	if len(request.args) > 0:
		# Si on a des arguments, on les joint avec la requête envoyée à l'API
		# On spécifie qu'on veut les données en format CSV avec -format=CSV
		search_query = ""
		for el in request.args:
			search_query += el + "=" + request.args.get(el) + "&"
		raw_res = requests.get(f"{api_url}ED&CO_DATE={periode}&{search_query}&-format=CSV")
	else:
		# Sinon on envoie la requête à l'API sans arguments de recherche
		raw_res = requests.get(f"{api_url}ED&CO_DATE={periode}&-format=CSV")
	# On prend juste la tranche après [Datas]\r\n de la réponse
	# C'est cette partie qui contient les enregistrements des communications
	# ici la variable _ contient la partie qu'on ne va pas utiliser
	_, res = raw_res.text.split("[Datas]\r\n")
	# On lit le CSV extrait comme se forme de dictionnaire
	reader = csv.DictReader(io.StringIO(res))
	# Puis on initialise la réponse qui va être retournée
	data = []
	# On ajoute chaque élément du dictionnaire généré à la réponse
	for row in reader:
		data.append(dict(row))
	else:
		for el in data:
			# Pour chaque enregitrement de communication, on convertit les durées
			# en secondes au format HH:MM:SS
			el['CO_DUR'] = str(datetime.timedelta(seconds = int(el['CO_DUR'])))
			el['CO_DRING'] = str(datetime.timedelta(seconds = int(el['CO_DRING'])))
			el['CO_DRTOT'] = str(datetime.timedelta(seconds = int(el['CO_DRTOT'])))
	# On retourne les données des communications en JSON à l'interface
	return jsonify(data)