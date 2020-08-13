import requests
import time, datetime
from flask import request, render_template, url_for, jsonify
from comtrafic_web import app

periode = "43666-43673"

@app.route("/")
def dashboard():
	return render_template("dashboard.html")

# @app.route("/dashboard-data")
# def dashboard_data():
# 	raw_res = requests.get(f"http://161.97.75.12:7071/api/cmd/ED&CO_DATE={periode}")
# 	res = raw_res.json()
# 	data = res["Data"]["Data"]
# 	c_communications = data["Lines"]
# 	postes = set()
# 	for item in data:
# 		postes.add(item['CO_EXT'])
# 	c_postes = len(postes)

postes = {'921', '935', '904', '902', '929', '949', '930', '932', '944', '900', '525', '928', '937', '933', '910', '931', '905', '907', '901', '934', '948', '938', '917', '922', '916', '912', '909', '903'}

services = {'Informatique', 'Support technique', 'Direction', 'Expéditions Stock', 'Technique', 'Achats Approvisionnements', 'Service_Defaut', 'Chambres', 'Compta', 'Commercial'}

@app.route("/communications")
def communications():
	return render_template("communications.html", postes=postes, services=services)

@app.route("/com-data")
def com_data():
	if len(request.args) > 0:
		search_query = ""
		for el in request.args:
			search_query += el + "=" + request.args.get(el) + "&"
		print(search_query)
		raw_res = requests.get(f"http://161.97.75.12:7071/api/cmd/ED&CO_DATE={periode}&{search_query}")
	else:
		raw_res = requests.get(f"http://161.97.75.12:7071/api/cmd/ED&CO_DATE={periode}")
	res = raw_res.json()
	data = res["Data"]["Data"]
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
	return render_template("cumuls.html")

@app.route("/cumuls-data")
def cumuls_data():
	response = requests.get("https://data.saroui.com/cumuls_data.json")
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
	response = requests.get("https://data.saroui.com/superv.json")
	data = response.json()
	return render_template("supervision.html", data=data)

@app.route("/facturation")
def facturation():
	return render_template("facturation.html")

@app.route("/facture-tableau")
def facture_tableau():
	return render_template("facture_tableau.html")

@app.route("/annuaires/annuaire-postes")
def annuaire_postes():
	response = requests.get("https://data.saroui.com/postes_data.json")
	data = response.json()
	return render_template("annuaires/annuaire_postes.html", data=data)

@app.route("/rapports")
def rapports():
	return render_template("rapports.html")

@app.route("/parametrage/parametrages")
def parametrages():
	return render_template("parametrage/parametrages.html")

@app.route("/parametrage/config-mails")
def config_mails():
	return render_template("parametrage/config_mails.html")

@app.route("/parametrage/tarifs-operateurs")
def tarifs_operateurs():
	return render_template("parametrage/tarifs_operateurs.html")

@app.route("/parametrage/liste-directions")
def liste_directions():
	return render_template("parametrage/liste_directions.html")

@app.route("/parametrage/droits-utilisateurs")
def droits_utilisateurs():
	return render_template("parametrage/droits_utilisateurs.html")
