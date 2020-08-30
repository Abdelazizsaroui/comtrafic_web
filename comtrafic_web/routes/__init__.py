import requests

api_port = 7072
api_url = f"http://161.97.75.12:{api_port}/api/cmd/"
periode = "43666-43673"

def etat_api():
	try:
		requests.get(f"http://161.97.75.12:{api_port}/api/", timeout=1)
		return 1
	except:
		return 0