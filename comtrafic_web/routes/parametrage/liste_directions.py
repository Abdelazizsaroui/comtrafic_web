from flask import render_template
from comtrafic_web import app
from comtrafic_web.routes import etat_api

@app.route("/parametrage/liste-directions")
def liste_directions():
	return render_template("parametrage/liste_directions.html", etat_api=etat_api())
