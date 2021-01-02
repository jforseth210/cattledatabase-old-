from flask import Flask, request, render_template
import json
import datetime
from operator import itemgetter
import pprint
pp = pprint.PrettyPrinter(indent=4)
app = Flask(__name__)


@app.route("/")
def homepage():
    q = request.args.get("q")
    if not q:
        with open("cows.json") as cows_file:
            cows_string = cows_file.read()
        cows_json = json.loads(cows_string)

        cows_table = []

        for owner in cows_json:
            owners_cows = cows_json[owner]
            owners_cows = sorted(
                owners_cows, key=lambda x: ([i[1] for i in owners_cows[x]["Events"] if i[0]  == "Born"]))
            pp.pprint(owners_cows)
            for cow in owners_cows:
                cows_table.append({
                    "uuid": cow,
                    "cow": cows_json[owner][cow]["Number"],
                    "born": [i[1] for i in cows_json[owner][cow]["Events"] if i[0]  == "Born"][0],
                    "owner": owner
                })
        return render_template("index.html", cows_table=cows_table)
    else:
        return render_template("search.html", query=q)


@app.route("/getcow")
def getcow():
    cowToGet = request.args.get("cow")
    with open("cows.json") as cows_file:
        cows_string = cows_file.read()
    cows_json = json.loads(cows_string)
    for owner in cows_json:
        for cow in cows_json[owner]:
            print(cow)
            if cow == cowToGet:
                return json.dumps(cows_json[owner][cow])

if __name__ == "__main__":
    app.debug = True
    app.run("0.0.0.0")
