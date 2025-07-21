from flask import Flask, session, render_template, request
from swimclub import read_swim_data

import os
import swimclub

app = Flask(__name__)
app.secret_key = "pares"
FOLDER = "/swimdata"

@app.get("/")
def index():
    return render_template("index.html", title="Welcome to the swimclub system!!")

def populate_data():
    if "swimmers" not in session:
        swim_files = os.listdir(swimclub.FOLDER)
        swim_files.remove('.DS_Store')
        session["swimmers"] = {}
        for file in swim_files:
            name, *_ = read_swim_data(file)
            if name not in session["swimmers"]:
                session["swimmers"][name] = []
            session["swimmers"][name].append(file)

@app.get("/swimmers")
def display_swimmers():
    populate_data()
    return render_template("select.html", title='Select a swimmer', data=sorted(session["swimmers"]), select_id='swimmer', url="/showfiles")
    # return str(sorted(session["swimmers"]))
    

@app.get("/file/<swimmer>")
def get_swimmer_files(swimmer):
    populate_data()
    return str(session["swimmers"][swimmer])

@app.post("/showfiles")
def display_swimmer_files():
    populate_data()
    name = request.form["swimmer"]
    return render_template("select.html",url="/showbarchart", select_id="file", title="Select an event", data=session["swimmers"][name])




if __name__ == "__main__":
    app.run(debug=True)