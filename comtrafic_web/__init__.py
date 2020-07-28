from flask import Flask

# Pas d'espaces aux cotés de '=' car ça peut générer des problèmes
app=Flask(__name__)

"""
=> Génération de la clé secrète: 
import secrets
secret_key = secrets.token_hex(16)
"""

app.config['SECRET_KEY'] = '96ac343ebb7bd6458f98231c3084fd29'

from comtrafic_web import routes