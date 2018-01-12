from flask import Flask, render_template, request, redirect
from firebase import firebase
from time import gmtime, strftime

app = Flask(__name__)
firebase = firebase.FirebaseApplication(
		'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', 
		authentication=None
	)

@app.route("/")

def main():
	tasks = firebase.get('/tasks', None)
	count = len(tasks.keys())
	completed = 0
	pending=0
	for key,task in tasks.items():
		if task['completed']:
			completed = completed+1
		else:
			pending = pending+1
	return render_template('index.html', active="main", total=count, pending=pending, completed=completed)

@app.route("/add", methods=["GET", "POST"])
def add():
	if request.method == 'POST':
		task = {
			'subject': request.form['subject'],
			'detail': request.form['detail'],
			'created': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
			'completed': '',
		}
		result = firebase.post('/tasks', task)
		return redirect("/list")
	else:
		return render_template('add.html', active="add")

@app.route("/list", methods=["GET"])
def list():
	tasks = firebase.get('/tasks', None)
	return render_template('list.html', active="list", tasks=tasks)

@app.route("/update", methods=["POST"])
def edit():
	if request.method == 'POST':
		# database = firebase.database()
		task = {
			'completed': strftime("%Y-%m-%d %H:%M:%S", gmtime())
		}
		result = firebase.patch('/tasks/'+request.form['key'], task)
		return 'update'
	else:
		main()

@app.route("/delete", methods=["DELETE"])
def delete():
	if request.method == 'DELETE':
		result = firebase.delete('/tasks',request.form['key'])
		return 'deleted'
	else:
		main()	

if __name__ == "__main__":
	app.run()