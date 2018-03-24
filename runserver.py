from flask import Flask
import os
import random
from flask.json import jsonify
from flask import render_template, url_for, request

app = Flask(__name__)




@app.route("/", methods=["GET"])
def test_doubles():
    file1, file2 = [ url_for('static', filename=file) for file in random.sample(files, 2)]

    return render_template("comparison.html", floorplan1=file1, floorplan2=file2)

@app.route("/", methods=["POST"])
def score_doubles():

    print(dict(request.form))

    which_button = request.form.get("plan")
    plan1 = request.form.get("plan1")
    plan2 = request.form.get("plan2")

    if which_button == "Right":
        plan1, plan2 = plan2, plan1

    if which_button == "Skip":
        return test_doubles()

    with open("./scores.txt", 'a') as f:
        f.write(f"{plan1} {plan2}\n")
    return test_doubles()



def read_files_to_be_scored(folder_path):
    for root, folders, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".svg"):
                yield file


if __name__ == "__main__":
    files = list(read_files_to_be_scored("./out"))
    app.run("127.0.0.1", 8600, debug=True)
