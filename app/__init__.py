import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

class TimelinePost(Model):
  name = CharField()
  email = CharField()
  content = TextField()
  created_at = DateTimeField(default=datetime.datetime.now)

  class Meta:
    database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_time_line_post(post_id):
    success = TimelinePost.delete_by_id(post_id)
    if success == 1:
        return {
            'message': f"Deleted post with id {post_id}"
        }
    else:
        return {
            'message': f"Cannot find post with id {post_id}"
        }

    

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]
    }


@app.route('/profile/<string:name>')
def portfolio(name):
    data = getData()

    portfolio_data = None
    for person in data:
        if person["name"].lower() == name.lower():
            portfolio_data = person

    if not portfolio_data:
        names = map(lambda x: x["name"].lower(), data)
        return render_template('index.html', title="The Ops Owls", url=os.getenv("URL"), names=names)

    return render_template("profile.html", portfolio_data=portfolio_data, api_key=os.getenv("GOOGLE_MAPS_API_KEY"))

@app.route('/timeline')
def timeline():
    posts = [model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]
    return render_template('timeline.html', title="Timeline", posts=posts)

@app.route('/')
def index():
    data = getData()
    names = map(lambda x: x["name"].lower(), data)
    return render_template('index.html', title="The Ops Owls", url=os.getenv("URL"), names=names)

def getData():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    with open(os.path.join(SITE_ROOT, "data.json")) as data_file:
        data = json.load(data_file)

    return data