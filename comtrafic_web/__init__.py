from flask import Flask

app=Flask(__name__)

"""
import secrets
secret_key = secrets.token_hex(16)
"""

app.config['SECRET_KEY'] = '96ac343ebb7bd6458f98231c3084fd29'

from comtrafic_web.routes import (
			dashboard,
			supervision,
			facturation,
			facture_tableau,
			communications,
			cumuls,
			rapports,
	)
from comtrafic_web.routes.annuaires import annuaire_postes
from comtrafic_web.routes.parametrage import (
			config_mails,
			droits_utilisateurs,
			liste_directions,
			parametrages,
			tarifs_operateurs
	)