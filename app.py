from flask import Flask, session, render_template, request
from swimclub import read_swim_data, produce_bar_chart, FOLDER

import os

app = Flask(__name__)
app.secret_key = "pares"
FOLDER = "/swimdata"

@app.get("/")
def index():
    return render_template("index.html", title="Welcome to the swimclub system!!")

def populate_data():
    if "swimmers" not in session:
        swim_files = os.listdir(FOLDER)
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

@app.post("/showbarchart")
def show_bar_chart():
    file_id = request.form["file"]
    location = produce_bar_chart(file_id, "templates/")
    return render_template(location.split("/"[-1]))




if __name__ == "__main__":
    app.run(debug=True)