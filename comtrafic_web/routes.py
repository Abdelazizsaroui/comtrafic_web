import requests
import time, datetime
from flask import Response, render_template, url_for, jsonify
from comtrafic_web import app


@app.route("/")
def dashboard():
	return render_template("dashboard.html")

@app.route("/communications")
def communications():
	return render_template("communications.html")

@app.route("/com-data")
def com_data():
	response = requests.get("https://data.saroui.com/com_data.json")
	data = response.json()
	for el in data:
		el['CO_DATE'] = el['CO_DATE'][:10] + " " + el['CO_DATE'][11:19]
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

@app.route("/facture-tab")
def facture_tab():
	return render_template("facture_tab.html")

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
