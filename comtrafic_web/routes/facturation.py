from flask import render_template
from comtrafic_web import app
from comtrafic_web.routes import etat_api

@app.route("/facturation")
def facturation():
	return render_template("facturation.html", etat_api=etat_api())