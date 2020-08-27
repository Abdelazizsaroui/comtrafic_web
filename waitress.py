from waitress import serve
from comtrafic_web import app

# Ceci permet de lancer l'application avec le serveur Waitress
if __name__ == '__main__':
	serve(app, host='0.0.0.0', port=80)