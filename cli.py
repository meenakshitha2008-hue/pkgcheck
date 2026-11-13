import json
import os
import sys
import urllib.parse
import urllib.request

API_URL = os.getenv("PKGCHECK_URL", "http://127.0.0.1:8000") + "/check"


def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py <package-name>")
        return
    name = sys.argv[1]
    url = API_URL + "?" + urllib.parse.urlencode({"name": name})
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.load(r)
    except Exception as e:
        print("Could not reach the pkgcheck server:", e)
        return
    line = f"{data['name']}   {data['verdict']}"
    if data["verdict"] == "RISKY" and data["reasons"]:
        line += " - " + "; ".join(data["reasons"])
    print(line)


if __name__ == "__main__":
    main()