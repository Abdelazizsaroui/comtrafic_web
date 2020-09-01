import requests, datetime
import xml.etree.ElementTree as ET
from flask import render_template, jsonify, request
from comtrafic_web import app
from comtrafic_web.routes import api_url, periode, etat_api

"""
Ces données Postes et Services sont utilisées
uniquement pour leurs listes dérolantes
corréspondates dans le forumulaire de filtrage
sur la page Communications.
Pour regénérer ces données, exécutez les scripts
sur le répértoire ./scripts
"""
postes = {'921', '935', '904', '902', '929', '949', '930', '932', '944', '900', '525', '928', '937', '933', '910', '931', '905', '907', '901', '934', '948', '938', '917', '922', '916', '912', '909', '903'}
services = {'Informatique', 'Support technique', 'Direction', 'Expéditions Stock', 'Technique', 'Achats Approvisionnements', 'Service_Defaut', 'Chambres', 'Compta', 'Commercial'}

@app.route("/communications")
def communications():
	return render_template("communications.html", etat_api=etat_api(), postes=postes, services=services)

@app.route("/communications/_xml_")
def communications_xml():
	return render_template("communications_xml.html", etat_api=etat_api(), postes=postes, services=services)

@app.route("/com-data")
def com_data():
	if len(request.args) > 0:
		search_query = ""
		for el in request.args:
			search_query += el + "=" + request.args.get(el) + "&"
		raw_res = requests.get(f"{api_url}ED&CO_DATE={periode}&{search_query}")
	else:
		raw_res = requests.get(f"{api_url}ED&CO_DATE={periode}")
	res = raw_res.json()
	data = res['Data']
	if data == "":
		data = []
	else:
		for el in data:
			el['CO_DUR'] = str(datetime.timedelta(seconds = el['CO_DUR']))
			el['CO_DRING'] = str(datetime.timedelta(seconds = el['CO_DRING']))
			el['CO_DRTOT'] = str(datetime.timedelta(seconds = el['CO_DRTOT']))
	return jsonify(data)

@app.route("/com-data-xml")
def com_data_xml():
	if len(request.args) > 0:
		search_query = ""
		for el in request.args:
			search_query += el + "=" + request.args.get(el) + "&"
		raw_res = requests.get(f"{api_url}ED&CO_DATE={periode}&{search_query}&-format=XML")
	else:
		raw_res = requests.get(f"{api_url}ED&CO_DATE={periode}&-format=XML")
	xml_root = ET.fromstring(raw_res.content)
	lines = xml_root[0][3].text[2:-1]
	n = int(lines)
	data = []
	for i in range(n):
		data.append(xml_root[2][i].attrib)
	else:
		for el in data:
			el['CO_DUR'] = str(datetime.timedelta(seconds = int(el['CO_DUR'])))
			el['CO_DRING'] = str(datetime.timedelta(seconds = int(el['CO_DRING'])))
			el['CO_DRTOT'] = str(datetime.timedelta(seconds = int(el['CO_DRTOT'])))
	return jsonify(data)