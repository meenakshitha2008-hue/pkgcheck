import requests, json

url = "https://raw.githubusercontent.com/DataDog/malicious-software-packages-dataset/main/samples/pypi/manifest.json"
data = requests.get(url).json()
names = list(data.keys())
print(len(names), names[:5])

with open("data/bad_names.json", "w") as f:
    json.dump(names, f)