import requests

raw_res = requests.get(f"http://161.97.75.12:7071/api/cmd/ED&CO_DATE=43666-43673")
res = raw_res.json()
data = res["Data"]["Data"]
services = set()
for item in data:
	services.add(item['SE_NOM'])
print(services)