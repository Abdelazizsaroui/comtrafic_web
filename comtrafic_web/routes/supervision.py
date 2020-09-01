import requests, datetime 
from flask import render_template, jsonify
from comtrafic_web import app
from comtrafic_web.routes import api_url, periode, etat_api

@app.route("/supervision")
def supervision():
	return render_template("supervision.html", etat_api=etat_api())

@app.route("/superv-data")
def superv_data():
	raw_res = requests.get(f"{api_url}ED&CO_DATE={periode}")
	res = raw_res.json()
	data = res['Data']
	postes_set = set()
	for el in data:
		postes_set.add(el['PO_NOM'])
	postes = [{"po_nom": value, "po_usernom": "",
			   "appels": 0, "duree": 0, "cout": 0}
			   for value in postes_set]
	for el in data:
		poste = [e for e in postes if e['po_nom'] == el['PO_NOM']][0]
		poste['po_usernom'] = el['PO_USERNOM']
		poste['appels'] += 1
		poste['duree'] += el['CO_DUR']
		poste['cout'] += el['CO_COUTFACT_TTC']
	for item in postes:
		item['duree'] = str(datetime.timedelta(seconds = item['duree']))

	return jsonify(postes)