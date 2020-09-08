# Le backend de la page Tableau de bord
# La page Tableau de bord existe sur l'interface en 3 versions
# connectées à l'API en JSON, XML et CSV

import requests, datetime
import csv, io
import xml.etree.ElementTree as ET
from flask import render_template, jsonify, request
from collections import Counter
from comtrafic_web import app
from comtrafic_web.routes import etat_api, periode, api_url

# Cette fonction serve la page statique «dashbord.html»
@app.route("/")
def dashboard():
	return render_template("dashboard.html", etat_api=etat_api())

# Cette fonction serve la page statique «dashbord_xml.html»
@app.route("/_xml_")
def dashboard_xml():
	return render_template("dashboard_xml.html", etat_api=etat_api())

# Cette fonction serve la page statique «dashbord_csv.html»
@app.route("/_csv_")
def dashboard_csv():
	return render_template("dashboard_csv.html", etat_api=etat_api())

# Cette fonction fournit les informations sur la base de donnée
# à la page «dashboard.html»
@app.route("/dashboard-db-info")
def dashboard_db_info():
	# On envoie une requête à l'API pour les données des communications
	raw_res = requests.get(f"{api_url}ED&CO_DATE={periode}")
	# Puis On extrait le contenu JSON de la réponse de l'API
	res = raw_res.json()
	# On extrait le nombre de communications
	c_communications = res['Infos']['Lines']
	# Puis la partie qui contient les données des communications
	data = res['Data']
	# On initialise les listes des postes, services et PBX
	services = set()
	postes = set()
	pbx = set()
	# Puis en fait une boucle sur les données pour populer les listes
	for item in data:
		services.add(item['SE_NOM'])
		postes.add(item['CO_EXT'])
		pbx.add(item['CO_PBX'])
	# Puis on compte le nombre de chaque élément
	c_services = len(services)
	c_postes = len(postes)
	c_pbx = len(pbx)
	# Et on retourne les données en JSON à l'interface
	return jsonify({"c_communications":c_communications, "c_postes": c_postes, "c_services": c_services, "c_pbx":c_pbx})

# Cette fonction fournit les informations sur la base de donnée
# à la page «dashboard_xml.html»
@app.route("/dashboard-db-info-xml")
def dashboard_db_info_xml():
	# On envoie une requête à l'API pour les données des communications
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
	# On extrait le nombre de communications
	c_communications = n
	# On initialise les listes des postes, services et PBX
	services = set()
	postes = set()
	pbx = set()
	# Puis en fait une boucle sur les données pour populer les listes
	for item in data:
		services.add(item['SE_NOM'])
		postes.add(item['CO_EXT'])
		pbx.add(item['CO_PBX'])
	# Puis on compte le nombre de chaque élément
	c_services = len(services)
	c_postes = len(postes)
	c_pbx = len(pbx)
	# Et on retourne les données en JSON à l'interface
	return jsonify({"c_communications":c_communications, "c_postes": c_postes, "c_services": c_services, "c_pbx":c_pbx})

# Cette fonction fournit les informations sur la base de donnée
# à la page «dashboard_csv.html»
@app.route("/dashboard-db-info-csv")
def dashboard_db_info_csv():
	# On envoie une requête à l'API pour les données des communications
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
	# On extrait le nombre de communications
	c_communications = len(data)
	# On initialise les listes des postes, services et PBX
	services = set()
	postes = set()
	pbx = set()
	# Puis en fait une boucle sur les données pour populer les listes
	for item in data:
		services.add(item['SE_NOM'])
		postes.add(item['CO_EXT'])
		pbx.add(item['CO_PBX'])
	# Puis on compte le nombre de chaque élément
	c_services = len(services)
	c_postes = len(postes)
	c_pbx = len(pbx)
	# Et on retourne les données en JSON à l'interface
	return jsonify({"c_communications":c_communications, "c_postes": c_postes, "c_services": c_services, "c_pbx":c_pbx})

# Cette fonction permet de fixer le format de sortie
# de datetime.timedelta et éliminer le mot «day»
def convert_days(d):
	if "day" in d:
		x,y = d.split(',')
		numb_d = int(x[0])
		h,m,s = y.split(':')
		int_h = int(h)
		int_h += numb_d * 24
		return str(int_h) + ':' + m + ':' + s
	return d

# Cette fonction fournit les données des communications pour
# le tableau et les graphiques de la page «dashboard.html»
@app.route("/dashboard-data")
def dashboard_data():
	# On teste si la requête vient avec des arguments (filtres de recherche)
	# Dans ce cas le seul argument qu'on peut joindre à la requête
	# est la plage de date : CO_DATE
	# La requête vient avec 0 arguments dans 2 cas:
	# 1 - Lorsque la page se charge
	# 2 - Lorsque on clique sur «Actualiser» avec la période complète
	if len(request.args) > 0:
		# Si on a l'argument CO_DATE, on le joint avec la requête envoyée à l'API
		# La réponse retournée par défaut est en JSON
		co_date = request.args.get('CO_DATE') if len(request.args.get('CO_DATE')) else periode
		raw_res = requests.get(f"{api_url}ED&CO_DATE={co_date}")
	else:
		# Sinon on envoie la requête à l'API pour la période complète
		raw_res = requests.get(f"{api_url}ED&CO_DATE={periode}")
	# On charge le contenu JSON de la réponse de l'API sur res
	res = raw_res.json()
	# On retient le nombre de lignes de communications
	c_all = res['Infos']['Lines']
	# Puis la partie Data qui contient les données des communications
	data = res['Data']
	# On crée et remplie un compteur des services
	# çad. le nom de chaque service et son nombre d'apparition
	c = Counter(el['SE_NOM'] for el in data)
	# Puis on le convertit en liste de dictionnaires
	services = [{'service':key, 'count':value} for key,value in c.items()]
	# On retient aussi juste les noms des services pour les utiliser dans les graphes
	services_set = {service for service,_ in c.items()}
	# Et on crée un dictionnaire pour les coûts des services
	couts_raw = {service:0 for service in services_set}
	# On fait une boucle sur les données des communications pour remplir
	# les coûts de services
	for el in data:
		couts_raw[el['SE_NOM']] += el['CO_COUTFACT_TTC']
	# Puis on fait un tri sur les coûts et on retient juste les top 5
	couts = {k: v for k, v in sorted(couts_raw.items(), key=lambda item: item[1], reverse=True)}
	top_couts = [{'service':key, 'cout':value} for key,value in couts.items()][:5]
	# Ici on commence le traitement des données du petit tableau
	# On initialise les variables
	c_entr = c_sort = 0
	d_all = d_entr = d_sort = 0;
	# Puis on fait uen boucle sur les données des communications calculer les variables
	for item in data:
		if item['CO_TYPE'] == 0:
			c_entr += 1
			d_add = item['CO_DUR']
			d_all += d_add
			d_entr += d_add
		elif item['CO_TYPE'] == 1:
			c_sort += 1
			d_add = item['CO_DUR']
			d_all += d_add
			d_sort += d_add
			
	# On covertit les durées en format : HH:MM:SS
	d_all_str = convert_days(str(datetime.timedelta(seconds = d_all))) 
	d_entr_str = convert_days(str(datetime.timedelta(seconds = d_entr)))
	d_sort_str = convert_days(str(datetime.timedelta(seconds = d_sort)))

	# Puis on retourne les données du tableau et des graphiques en JSON
	return jsonify({
			"all": {"c": c_all, "d": d_all_str},
			"entr": {"c": c_entr, "d": d_entr_str},
			"sort": {"c": c_sort, "d": d_sort_str},
			"services": services,
			"top_couts": top_couts
		})

# Cette fonction fournit les données des communications pour
# le tableau et les graphiques de la page «dashboard_xml.html»
@app.route("/dashboard-data-xml")
def dashboard_data_xml():
	# On teste si la requête vient avec des arguments (filtres de recherche)
	# Dans ce cas le seul argument qu'on peut joindre à la requête
	# est la plage de date : CO_DATE
	# La requête vient avec 0 arguments dans 2 cas:
	# 1 - Lorsque la page se charge
	# 2 - Lorsque on clique sur «Actualiser» avec la période complète
	if len(request.args) > 0:
		# Si on a l'argument CO_DATE, on le joint avec la requête envoyée à l'API
		# La réponse retournée par défaut est en JSON
		co_date = request.args.get('CO_DATE') if len(request.args.get('CO_DATE')) else periode
		raw_res = requests.get(f"{api_url}ED&CO_DATE={co_date}&-format=XML")
	else:
		# Sinon on envoie la requête à l'API pour la période complète
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
	# On initialise la liste des données des communications
	data = []
	# On joint chaque ligne de communication à la liste
	# xml[2][i].attrib retourne un dictionnaire avec les noms 
	# et les valeurs de chaque champ comme en JSON
	for i in range(n):
		data.append(xml_root[2][i].attrib)
	# On retient le nombre de lignes de communications
	c_all = n
	# On crée et remplie un compteur des services
	# çad. le nom de chaque service et son nombre d'apparition
	c = Counter(el['SE_NOM'] for el in data)
	# Puis on le convertit en liste de dictionnaires
	services = [{'service':key, 'count':value} for key,value in c.items()]
	# On retient aussi juste les noms des services pour les utiliser dans les graphes
	services_set = {service for service,_ in c.items()}
	# Et on crée un dictionnaire pour les coûts des services
	couts_raw = {service:0 for service in services_set}
	# On fait une boucle sur les données des communications pour remplir
	# les coûts de services
	for el in data:
		couts_raw[el['SE_NOM']] += float(el['CO_COUTFACT_TTC'])
	# Puis on fait un tri sur les coûts et on retient juste les top 5
	couts = {k: v for k, v in sorted(couts_raw.items(), key=lambda item: item[1], reverse=True)}
	top_couts = [{'service':key, 'cout':value} for key,value in couts.items()][:5]
	# Ici on commence le traitement des données du petit tableau
	# On initialise les variables
	c_entr = c_sort = 0
	d_all = d_entr = d_sort = 0;
	# Puis on fait uen boucle sur les données des communications calculer les variables
	for item in data:
		if item['CO_TYPE'] == '0':
			c_entr += 1
			d_add = int(item['CO_DUR'])
			d_all += d_add
			d_entr += d_add
		elif item['CO_TYPE'] == '1':
			c_sort += 1
			d_add = int(item['CO_DUR'])
			d_all += d_add
			d_sort += d_add
	
	# On covertit les durées en format : HH:MM:SS
	d_all_str = convert_days(str(datetime.timedelta(seconds = d_all))) 
	d_entr_str = convert_days(str(datetime.timedelta(seconds = d_entr)))
	d_sort_str = convert_days(str(datetime.timedelta(seconds = d_sort)))

	# Puis on retourne les données du tableau et des graphiques en JSON
	return jsonify({
			"all": {"c": c_all, "d": d_all_str},
			"entr": {"c": c_entr, "d": d_entr_str},
			"sort": {"c": c_sort, "d": d_sort_str},
			"services": services,
			"top_couts": top_couts
		})

@app.route("/dashboard-data-csv")
def dashboard_data_csv():
	if len(request.args) > 0:
		co_date = request.args.get('CO_DATE') if len(request.args.get('CO_DATE')) else periode
		raw_res = requests.get(f"{api_url}ED&CO_DATE={co_date}&-format=CSV")
	else:
		raw_res = requests.get(f"{api_url}ED&CO_DATE={periode}&-format=CSV")
	_, res = raw_res.text.split("[Datas]\r\n")
	reader = csv.DictReader(io.StringIO(res))
	data = []
	for row in reader:
		data.append(dict(row))
	c_all = len(data)
	c = Counter(el['SE_NOM'] for el in data)
	services = [{'service':key, 'count':value} for key,value in c.items()]
	services_set = {service for service,_ in c.items()}
	couts_raw = {service:0 for service in services_set}
	for el in data:
		couts_raw[el['SE_NOM']] += float(el['CO_COUTFACT_TTC'])
	couts = {k: v for k, v in sorted(couts_raw.items(), key=lambda item: item[1], reverse=True)}
	top_couts = [{'service':key, 'cout':value} for key,value in couts.items()][:5]
	c_entr = c_sort = 0
	d_all = d_entr = d_sort = 0;
	for item in data:
		if item['CO_TYPE'] == '0':
			c_entr += 1
			d_add = int(item['CO_DUR'])
			d_all += d_add
			d_entr += d_add
		elif item['CO_TYPE'] == '1':
			c_sort += 1
			d_add = int(item['CO_DUR'])
			d_all += d_add
			d_sort += d_add
			
	d_all_str = convert_days(str(datetime.timedelta(seconds = d_all))) 
	d_entr_str = convert_days(str(datetime.timedelta(seconds = d_entr)))
	d_sort_str = convert_days(str(datetime.timedelta(seconds = d_sort)))

	return jsonify({
			"all": {"c": c_all, "d": d_all_str},
			"entr": {"c": c_entr, "d": d_entr_str},
			"sort": {"c": c_sort, "d": d_sort_str},
			"services": services,
			"top_couts": top_couts
		})