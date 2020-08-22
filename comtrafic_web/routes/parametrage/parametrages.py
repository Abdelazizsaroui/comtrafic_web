from flask import render_template
from comtrafic_web import app
from comtrafic_web.routes import etat_api

@app.route("/parametrage/parametrages")
def parametrages():
	return render_template("parametrage/parametrages.html", etat_api=etat_api())