from flask import Flask, request
from  flask import render_template
from pymongo import MongoClient
import datetime, json
import uuid

db_client = MongoClient()
db = db_client.help
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('home.html')

@app.route("/create")
def create():
    return render_template('create_post.html')

@app.route("/view")
def view():
	return render_template('view_post.html')

@app.route("/createpost", methods = ['POST'])
def create_post():
	title = request.json.get("help_title")
	subject = request.json.get("help_subject")
	job_id = str(uuid.uuid4()) 
	obj = {"data":{"help_title":title, "help_subject":subject, "created_on":datetime.datetime.utcnow(), 
			"job_id":job_id}}
	try:
		db.posts.insert(obj)
	except:
		return json.dumps({"success":False})
	return json.dumps({"success":True})


@app.route("/viewpost", methods = ['POST'])
def view_post():
	filter_data = request.json.get("filter")
	posts = []
	if not filter_data:
		cur = db.posts.find()
		for i in cur:
			data = i["data"]
			data["created_on"] = str(data["created_on"])
			posts.append(data)
		return json.dumps(posts)



if __name__ == "__main__":
    app.run()