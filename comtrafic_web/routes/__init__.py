# Ce fichier déclare «routes» comme un module de python
# il contient les variables et les fonctions qui sont communs
# à tous les les autres fichiers.

# Le module request est utilisé pour se connecter à l'API via HTTP
import requests

# Le port sur lequel l'API est servie dans le serveur
api_port = 7071

# L'URL de l'API
api_url = f"http://161.97.75.12:{api_port}/api/cmd/"

# La période définie comme la période complète dont on peut
# Extraire les communications de l'API
periode = "43666-43673"

# Etat de l'API est un test pour s'assurer que la connexion à l'API
# est réussie à chaque chargement de l'interface, ceci est utile
# pour savoir en cas de problème avec l'interface si la connexion à l'API
# qui a causé le problème.
# «timeout=1» déclare le temps maximale (1 seconde) que peut durée le test
# avant de le considérer échoué.
def etat_api():
	try:
		requests.get(f"http://161.97.75.12:{api_port}/api/", timeout=1)
		return 1
	except:
		return 0