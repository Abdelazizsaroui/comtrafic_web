import requests, datetime 
from flask import render_template, jsonify, request
from collections import Counter
from comtrafic_web import app
from comtrafic_web.routes import api_url, periode, etat_api

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