import os
import json

from app import History
from graph import Graph
from flask import Flask, render_template, request, url_for

UPLOAD_DIR = "upload"
DB_DIR = "db"
# создать папку если ее нет
MAX_FILE_SIZE = 1024 * 1024

app = Flask(__name__)

hist = None


@app.route("/")
def index():
    return render_template("template.html", hist=hist.tolist())


@app.route("/id")
def get_id():
    value = hist.history[-1]
    print(value)
    return '<li id="{}">{}</li>'.format(value[0], ' '.join(value[1:]))


@app.route("/graph")
def graph():
    try:
        idx = int(request.args.get('id', None))
        filename = hist[idx][2]
        fullpath = os.path.join(UPLOAD_DIR, filename)
        g = Graph(fullpath)
        return g.to_visjs()
    except Exception as e:  # вернуть код ощтюбки
        print("--", e)
        return json.dumps({})


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if not file.filename:
        raise Exception('no file name.')

    fullpath = os.path.join(UPLOAD_DIR, file.filename)
    file.save(fullpath)
    hist.add(fullpath)
    return "OK"


def create_dir(root_dir):
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)


if __name__ == "__main__":
    create_dir('db')
    create_dir('upload')
    hist = History(os.path.join(DB_DIR, 'db.csv'))

    app.run(debug=True)
