import json
import random
import urllib.parse
import urllib.request

random.seed(1)
with open("data/good_names.json") as f:
    good = json.load(f)

names = random.sample(good[1000:], 30)
for _ in range(30):
    length = random.randint(8, 16)
    names.append("".join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(length)))

for n in names:
    url = "http://127.0.0.1:8000/check?" + urllib.parse.urlencode({"name": n})
    urllib.request.urlopen(url, timeout=30).read()
print("sent", len(names), "checks")