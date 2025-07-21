from flask import Flask, session, render_template
from swimclub import read_swim_data

import os
import swimclub

app = Flask(__name__)
app.secret_key = "pares"
FOLDER = "/swimdata"

@app.get("/")
def index():
    return "pop"

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
    return str(sorted(session["swimmers"]))
    

@app.get("/file/<swimmer>")
def get_swimmer_Files(swimmer):
    populate_data()
    return str(session["swimmers"][swimmer])




if __name__ == "__main__":
    app.run(debug=True)