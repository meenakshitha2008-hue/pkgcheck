import requests, json

url = "https://hugovk.dev/top-pypi-packages/top-pypi-packages.min.json"
data = requests.get(url).json()
good = [row["project"] for row in data["rows"][:5000]]

with open("data/bad_names.json") as f:
    bad = json.load(f)

good = [n for n in good if n not in bad]
print(len(good), good[:5])

with open("data/good_names.json", "w") as f:
    json.dump(good, f)