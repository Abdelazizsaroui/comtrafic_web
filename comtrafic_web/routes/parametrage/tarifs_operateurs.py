from flask import render_template
from comtrafic_web import app
from comtrafic_web.routes import etat_api

@app.route("/parametrage/tarifs-operateurs")
def tarifs_operateurs():
	return render_template("parametrage/tarifs_operateurs.html", etat_api=etat_api())