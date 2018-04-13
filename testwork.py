import os
import json

from storage import History
from flask import Flask, render_template, request, url_for

app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'graphs.db')
))

storage = None

@app.route("/")
def index():
    return render_template("template.html", table=storage.tolist())


@app.route("/id")
def get_id():
    value = storage.get_metadata_by_id(-1)
    print(value)
    return '<li id="{}">{}</li>'.format(value[0], ' '.join(value[1:]))


@app.route("/graph")
def graph():
    try:
        idx = int(request.args.get('id', -1))
        return storage.get_graph_by_id(idx)
    except Exception as e:  # вернуть код ощтюбки
        print("Error in <graph()> :", e)
        return json.dumps({})


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    try:
        storage.save(file)
    except Exception as err:
        print('Error in <upload>: ', err)
    return "OK"


if __name__ == "__main__":

    storage = History(app.config['DATABASE'])
    app.run(debug=True)
