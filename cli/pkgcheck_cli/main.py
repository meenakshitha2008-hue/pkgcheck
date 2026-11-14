import json
import os
import sys
import urllib.parse
import urllib.request

BASE_URL = os.getenv("PKGCHECK_URL", "https://pkgcheck.onrender.com")


def main():
    if len(sys.argv) < 2:
        print("Usage: pkgcheck <package-name>")
        return
    name = sys.argv[1]
    url = BASE_URL + "/check?" + urllib.parse.urlencode({"name": name})
    try:
        with urllib.request.urlopen(url, timeout=90) as r:
            data = json.load(r)
    except Exception as e:
        print("Could not reach the pkgcheck server:", e)
        print("If the server was idle, wait a minute and try again.")
        return
    line = f"{data['name']}   {data['verdict']}"
    if data["verdict"] == "RISKY" and data["reasons"]:
        line += " - " + "; ".join(data["reasons"])
    print(line)


if __name__ == "__main__":
    main()