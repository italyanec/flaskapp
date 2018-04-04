from flask import Flask, render_template, request, url_for
import os
from app import History
from graph import Graph

UPLOAD_DIR = "upload"
DB_DIR = "db"
# создать папку если ее нет
MAX_FILE_SIZE = 1024 * 1024

app = Flask(__name__)

hist = History(os.path.join(DB_DIR, 'db.csv'))

@app.route("/", methods=["POST", "GET"])
def index():
    args = {} 
    if request.method == "POST":
        file = request.files["file"]
        if bool(file.filename):
            file_bytes = file.read(MAX_FILE_SIZE)
            args["file_size_error"] = len(file_bytes) == MAX_FILE_SIZE
            if not args["file_size_error"]:
                filename = file.filename
                fullpath = os.path.join(UPLOAD_DIR, filename)
                file.save(fullpath)
                hist.add(fullpath)
        args["method"] = "POST"
    else:
        args["method"] = "GET"
    #print(url_for('static', filename='vis.js'))
    return render_template("template.html", args=args, hist=hist.tolist())

@app.route("/graph")
def graph():
    print(request.args.get('id', 0))
    return Graph('sample.xlsx').to_visjs()

if __name__ == "__main__":
    app.run()#debug=True
