import requests
from flask import render_template, jsonify
from comtrafic_web import app
from comtrafic_web.routes import api_url, periode, etat_api

@app.route("/annuaires/annuaire-postes")
def annuaire_postes():
	return render_template("annuaires/annuaire_postes.html", etat_api=etat_api())

@app.route("/annuaires/annuaire-postes-data")
def annuaire_postes_data():
	raw_res = requests.get(f"{api_url}ED&CO_DATE={periode}")
	res = raw_res.json()
	data = res['Data']
	services_set = set()
	for el in data:
		services_set.add(el['SE_NOM'])
	services = [{"nom": service, "count": 0} for service in services_set]
	postes = []
	excl = []
	for el in data:
		service = [e for e in services if e['nom'] == el['SE_NOM']][0]
		if not el['PO_NOM'] in excl:
			excl.append(el['PO_NOM'])
			service['count'] += 1
			poste = {"poste": el['PO_NOM'], "nom": el['PO_USERNOM'], "prenom": el['PO_USERPRENOM'], "service": el['SE_NOM'], "date": el['PO_DATE']}
			postes.append(poste)
	for el in postes:
		date,_ = el['date'].split("T")
		el['date'] = date
	postes_c = len(postes)
	response = {"services": services, "postes": postes, "postes_c": postes_c}

	return jsonify(response)