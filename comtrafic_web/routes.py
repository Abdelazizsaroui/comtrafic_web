import requests
import time, datetime
from collections import Counter
from flask import request, render_template, url_for, jsonify
from comtrafic_web import app

api_url = "http://161.97.75.12:7071/api/cmd/"
periode = "43666-43673"

def etat_api():
	try:
		requests.get("http://161.97.75.12:7071/api/", timeout=1)
		return 1
	except:
		return 0

@app.route("/")
def dashboard():
	return render_template("dashboard.html", etat_api=etat_api())

@app.route("/dashboard-db-info")
def dashboard_db_info():
	raw_res = requests.get(f"{api_url}ED&CO_DATE={periode}")
	res = raw_res.json()
	c_communications = res['Data']['Lines']
	data = res['Data']['Data']
	services = set()
	postes = set()
	pbx = set()
	for item in data:
		services.add(item['SE_NOM'])
		postes.add(item['CO_EXT'])
		pbx.add(item['CO_PBX'])
	c_services = len(services)
	c_postes = len(postes)
	c_pbx = len(pbx)
	return jsonify({"c_communications":c_communications, "c_postes": c_postes, "c_services": c_services, "c_pbx":c_pbx})

@app.route("/dashboard-data")
def dashboard_data():
	if len(request.args) > 0:
		co_date = request.args.get('CO_DATE') if len(request.args.get('CO_DATE')) else periode
		raw_res = requests.get(f"{api_url}ED&CO_DATE={co_date}")
	else:
		raw_res = requests.get(f"{api_url}ED&CO_DATE={periode}")
	res = raw_res.json()
	c_all = res['Data']['Lines']
	data = res['Data']['Data']
	c = Counter(el['SE_NOM'] for el in data)
	services = [{'service':key, 'count':value} for key,value in c.items()]
	services_set = {service for service,_ in c.items()}
	couts_raw = {service:0 for service in services_set}
	for el in data:
		couts_raw[el['SE_NOM']] += el['CO_COUTFACT_TTC']
	couts = {k: v for k, v in sorted(couts_raw.items(), key=lambda item: item[1], reverse=True)}
	top_couts = [{'service':key, 'cout':value} for key,value in couts.items()][:5]
	c_entr = c_sort = 0
	d_all = d_entr = d_sort = 0;
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
	d_all_str = str(datetime.timedelta(seconds = d_all))
	d_entr_str = str(datetime.timedelta(seconds = d_entr))
	d_sort_str = str(datetime.timedelta(seconds = d_sort))
	return jsonify({
			"all": {"c": c_all, "d": d_all_str},
			"entr": {"c": c_entr, "d": d_entr_str},
			"sort": {"c": c_sort, "d": d_sort_str},
			"services": services,
			"top_couts": top_couts
		})
		
	
postes = {'921', '935', '904', '902', '929', '949', '930', '932', '944', '900', '525', '928', '937', '933', '910', '931', '905', '907', '901', '934', '948', '938', '917', '922', '916', '912', '909', '903'}

services = {'Informatique', 'Support technique', 'Direction', 'Expéditions Stock', 'Technique', 'Achats Approvisionnements', 'Service_Defaut', 'Chambres', 'Compta', 'Commercial'}

@app.route("/communications")
def communications():
	return render_template("communications.html", etat_api=etat_api(), postes=postes, services=services)

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
	data = res['Data']['Data']
	if data == "":
		data = []
	else:
		for el in data:
			el['CO_DUR'] = str(datetime.timedelta(seconds = el['CO_DUR']))
			el['CO_DRING'] = str(datetime.timedelta(seconds = el['CO_DRING']))
			el['CO_DRTOT'] = str(datetime.timedelta(seconds = el['CO_DRTOT']))
	# return Response(data, status=200, mimetype='application/json')
	return jsonify(data)

@app.route("/cumuls")
def cumuls():
	return render_template("cumuls.html", etat_api=etat_api())

@app.route("/cumuls-data")
def cumuls_data():
	response = requests.get("https://data.saroui.com/cumuls_data.json")
	# raw_res = requests.get(f"{api_url}ED&CO_DATE={periode}")
	# res = raw_res.json()
	# data = res['Data']['Data']
	data = response.json()
	for el in data:
		el['CO_DUR'] = str(datetime.timedelta(seconds = el['CO_DUR']))
		el['CO_DURM'] = time.strftime("%H:%M:%S", time.gmtime(el['CO_DURM']))
		el['CO_DRING'] = str(datetime.timedelta(seconds = el['CO_DRING']))
		el['CO_DRINGM'] = time.strftime("%H:%M:%S", time.gmtime(el['CO_DRINGM']))
		try:
			el['CO_DUR_IN'] = str(datetime.timedelta(seconds = el['CO_DUR_IN']))
		except:
			pass
		try:
			el['CO_DUR_OUT'] = str(datetime.timedelta(seconds = el['CO_DUR_OUT']))
		except:
			pass
	return jsonify(data)

@app.route("/supervision")
def supervision():
	return render_template("supervision.html", etat_api=etat_api())

@app.route("/superv-data")
def superv_data():
	raw_res = requests.get(f"{api_url}ED&CO_DATE={periode}")
	res = raw_res.json()
	data = res['Data']['Data']
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

@app.route("/facturation")
def facturation():
	return render_template("facturation.html", etat_api=etat_api())

@app.route("/facture-tableau")
def facture_tableau():
	return render_template("facture_tableau.html", etat_api=etat_api())

@app.route("/annuaires/annuaire-postes")
def annuaire_postes():
	response = requests.get("https://data.saroui.com/postes_data.json")
	data = response.json()
	return render_template("annuaires/annuaire_postes.html", etat_api=etat_api(), data=data)

@app.route("/rapports")
def rapports():
	return render_template("rapports.html", etat_api=etat_api())

@app.route("/parametrage/parametrages")
def parametrages():
	return render_template("parametrage/parametrages.html", etat_api=etat_api())

@app.route("/parametrage/config-mails")
def config_mails():
	return render_template("parametrage/config_mails.html", etat_api=etat_api())

@app.route("/parametrage/tarifs-operateurs")
def tarifs_operateurs():
	return render_template("parametrage/tarifs_operateurs.html", etat_api=etat_api())

@app.route("/parametrage/liste-directions")
def liste_directions():
	return render_template("parametrage/liste_directions.html", etat_api=etat_api())

@app.route("/parametrage/droits-utilisateurs")
def droits_utilisateurs():
	return render_template("parametrage/droits_utilisateurs.html", etat_api=etat_api())
