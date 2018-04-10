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


@app.route("/graph")
def graph():
    idx = int(request.args.get('id', 0))
    print(idx)
    if idx < 0 or not idx:
        idx = hist.lastid

    if not idx:
        return json.dumps({})

    try:
        filename = hist[idx][0]
    except KeyError:
        raise Exception
        # вернуть код ощтюбки
    try:
        fullpath = os.path.join(UPLOAD_DIR, filename)
        g = Graph(fullpath)
    except Exception as e:
        print(e)
        raise Exception
        # вернуть код ощтюбки
    return g.to_visjs()


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if not file.filename:
        raise Exception('no file name.')

    fullpath = os.path.join(UPLOAD_DIR, file.filename)
    file.save(fullpath)
    hist.add(fullpath)
    return "OK"

@app.route("/id")
def getid():
    print(hist[hist.lastid])
    print('<li id="{}">{}</li>'.format(hist.lastid, ' '.join(hist[hist.lastid][::-1])))
    return '<li id="{}">{}</li>'.format(hist.lastid, ' '.join(hist[hist.lastid][::-1]))


def create_dir(root_dir):
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)


if __name__ == "__main__":
    create_dir('db')
    create_dir('upload')
    hist = History(os.path.join(DB_DIR, 'db.csv'))

    app.run(debug=True)
