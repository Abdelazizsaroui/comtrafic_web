import requests
from flask import render_template, request, jsonify
from comtrafic_web import app
from comtrafic_web.routes import api_url, periode, etat_api

@app.route("/facture-tableau")
def facture_tableau():
	return render_template("facture_tableau.html", etat_api=etat_api())

@app.route("/facture-tableau-data")
def facture_tableau_data():
	if len(request.args) > 0:
		search_query = ""
		for el in request.args:
			search_query += el + "=" + request.args.get(el) + "&"
		raw_res = requests.get(f"{api_url}FF&CO_DATE={periode}&{search_query}")
	else:
		raw_res = requests.get(f"{api_url}FF&CO_DATE={periode}")
	res = raw_res.json()
	data = res['Data']['Data']
	if data == "":
		data = []
	return jsonify(data)
