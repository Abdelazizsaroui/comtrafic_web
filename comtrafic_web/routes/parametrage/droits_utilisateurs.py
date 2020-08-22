from flask import render_template
from comtrafic_web import app
from comtrafic_web.routes import etat_api

@app.route("/parametrage/droits-utilisateurs")
def droits_utilisateurs():
	return render_template("parametrage/droits_utilisateurs.html", etat_api=etat_api())