### Interface web pour ComTrafic : 
[https://stage.saroui.com](https://stage.saroui.com)
 

**Structure du projet**

 - `comtrafic_web` : le répertoire principal du projet.
	 - `static` : contient les fichiers statiques (css/js/images ..).
		 - `dist` : contient les fichiers d'AdminLTE.
		 - `plugins` : contient les dépendances d'AdminLTE.
		 - ... et d'autres fichiers.
	- `templates` : contient les pages de l'interface.
		- `_base.html` : la page de base, elle est héritée par les autres pages. Elles contient les bloques communs entre toutes les pages.
		- .. et les autres pages.
	- `__init__.py` : déclare le répertoire comtrafic_web comme un module python et contient l'initialisation de l'application.
	- `routes` :  contient les fichiers de routage et des traitements en Python.
- `docs` : la documentation de l'interface et de déploiement.  
- `Procfile` : fichier nécessaire pour le déploiement sur Heroku. Il déclare `run.py` comme l'entrée de l'application pour le serveur web.
- `requirements.txt` : contient les dépendances du projet.
- `run.py` : le script pour démarrer l'application.


**Installation (test et dev):**

 - (*optionnel*) Configurer et activer un environnement virtuel de Python (venv, virtualenv .. )
 - Récupérer le dépot du projet :  
 **`$ git clone https://gitlab.com/prost.phil/interface-web-pour-comtrafic`** 

 - Installer les dépendances :  
 **`$ pip install -r requirements.txt`**

 - Lancer le serveur de développement :  
 **`$ python run.py`**

 - L'application est servie sur *localhost:5000*


**Déploiement (production):**

 - Linux sur une IaaS (Microsoft Azure) : [http://40.89.168.98](http://40.89.168.98)
 - Linux sur une PaaS (Heroku) : [https://stage.saroui.com](https://stage.saroui.com)
 - Windows : [http://161.97.75.12](http://161.97.75.12) (inactive)

 Le guide de dépoiement se trouve sur `docs/deploy.html`

