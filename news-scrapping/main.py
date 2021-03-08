import requests
from flask import Flask, render_template, request

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
    return f"{base_url}/items/{id}"


db = {}
app = Flask("DayNine")


@app.route("/")
def home():
    click = (request.args.get("order_by"))
    if click not in db:
        if click == "popular":
            url = popular
        else:
            url = new
        result = requests.get(url)
        results = result.json()["hits"]
        db[click] = results
        return render_template("index.html", clickBy=click, results=results)
    results = db[click]
    return render_template("index.html", clickBy=click, results=results)


@app.route("/<id>")
def change_id(id):
    url = make_detail_url(id)
    detail_result = requests.get(url)
    detail_results = detail_result.json()
    comments = detail_result.json()["children"]
    return render_template("detail.html", detail_results=detail_results, comments=comments)


app.run(host="0.0.0.0")
