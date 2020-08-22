import requests

api_url = "http://161.97.75.12:7071/api/cmd/"
periode = "43666-43673"

def etat_api():
	try:
		requests.get("http://161.97.75.12:7071/api/", timeout=1)
		return 1
	except:
		return 0