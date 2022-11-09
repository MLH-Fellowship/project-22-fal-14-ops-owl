import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from peewee import *
import json
import datetime
import re
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb =SqliteDatabase('file:memory?mode=memory&cache=shared',
uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306
)

# mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
#     user=os.getenv("MYSQL_USER"),
#     password=os.getenv("MYSQL_PASSWORD"),
#     host=os.getenv("MYSQL_HOST"),
#     port=3306
# )

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

print(mydb)

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    try:
        name = request.form['name']
    except Exception as e:
        return "Invalid name", 400
    else:
        if name == '':
            return "Invalid name", 400
    
    try:
        email = request.form['email']
    except Exception as e:
        return "Invalid email", 400
    else:
        if email == '':
            return "Invalid email", 400

    try:
        content = request.form['content']
    except Exception as e:
        return "Invalid content", 400
    else:
        if content == '':
            return "Invalid content", 400

    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        return "Invalid email", 400
    
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)


# @app.route('/api/timeline_post', methods=['POST'])
# def post_time_line_post():
#     # name =request.form['name']
#     # email= request.form['email']
#     # content=request.form['content']
#     name = request.form.get('name')
#     email = request.form.get('email', '')
#     content = request.form.get('content')
#     print(email)
#     print(name)
#     print(content)
#     if not all([name, re.match(r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", email), content]):
#         return jsonify("Invalid input"), 400

    # timeline_post = TimelinePost.create(name=name, email=email, content=content)
    # return model_to_dict(timeline_post)

@app.route("/api/timeline_post", methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

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

@app.route('/timeline')
def timeline():
    timeline_posts = [model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.
    created_at.desc())]
    return render_template('timeline.html', title="MLH Fellow - Timeline", url=os.getenv("URL"), timeline_posts=timeline_posts)

def getData():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    data_file = open(os.path.join(SITE_ROOT, "data.json"))
    data = json.load(data_file)

    return data

