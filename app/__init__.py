import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    data = getData()
    names = map(lambda x: x["name"].lower(), data)
    return render_template('index.html', title="The Ops Owlsss", url=os.getenv("URL"), names=names)

@app.route('/profile/<string:name>')
def portfolio(name):
    data = getData()

    portfolio_data = None
    for person in data:
        if person["name"].lower() == name.lower():
            portfolio_data = person

    if not portfolio_data:
        names = map(lambda x: x["name"].lower(), data)
        return render_template('index.html', title="The Ops Owlsss", url=os.getenv("URL"), names=names)

    return render_template("profile.html", portfolio_data=portfolio_data, api_key=os.getenv("GOOGLE_MAPS_API_KEY"))


def getData():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    data_file = open(os.path.join(SITE_ROOT, "data.json"))
    data = json.load(data_file)

    return data