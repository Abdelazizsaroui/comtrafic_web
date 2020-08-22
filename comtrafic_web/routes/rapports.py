from flask import render_template
from comtrafic_web import app
from comtrafic_web.routes import etat_api

@app.route("/rapports")
def rapports():
	return render_template("rapports.html", etat_api=etat_api())