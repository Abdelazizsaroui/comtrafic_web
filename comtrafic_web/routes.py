import requests
import json
import datetime
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
	response = requests.get("https://stage.saroui.com/com_data.json")
	data = response.json()
	for el in data:
		el['CO_DATE'] = el['CO_DATE'][:10] + " " + el['CO_DATE'][11:19]
		# el['CO_DUR'] = time.strftime("%H:%M:%S", time.gmtime(el['CO_DUR']))
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
	response = requests.get("https://stage.saroui.com/cumuls_data.json")
	data = response.json()
	# for el in data:
	# 	el['CO_DATE'] = el['CO_DATE'][:10] + " " + el['CO_DATE'][11:19]
	# 	el['CO_DUR'] = str(datetime.timedelta(seconds = el['CO_DUR']))
	# 	el['CO_DRING'] = str(datetime.timedelta(seconds = el['CO_DRING']))
	# 	el['CO_DRTOT'] = str(datetime.timedelta(seconds = el['CO_DRTOT'])) 
	return jsonify(data)