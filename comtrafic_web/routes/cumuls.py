import requests, time, datetime
from flask import render_template, jsonify
from comtrafic_web import app
from comtrafic_web.routes import api_url, periode, etat_api

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