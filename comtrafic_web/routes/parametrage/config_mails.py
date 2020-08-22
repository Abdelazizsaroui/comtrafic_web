from flask import render_template
from comtrafic_web import app
from comtrafic_web.routes import etat_api

@app.route("/parametrage/config-mails")
def config_mails():
	return render_template("parametrage/config_mails.html", etat_api=etat_api())