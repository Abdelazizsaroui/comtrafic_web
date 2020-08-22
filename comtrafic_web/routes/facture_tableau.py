from flask import render_template
from comtrafic_web import app
from comtrafic_web.routes import etat_api

@app.route("/facture-tableau")
def facture_tableau():
	return render_template("facture_tableau.html", etat_api=etat_api())