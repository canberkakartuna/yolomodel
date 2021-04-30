from flask import Flask, render_template, request, redirect, url_for, send_file
import redis
from rq import Queue
from tasks import prediction
import os

app = Flask(__name__)

# r = redis.Redis()
# q = Queue(connection=r)

RESULT_FOLDER = os.path.join('static')
app.config['RESULT_FOLDER'] = RESULT_FOLDER

@app.route("/", methods=["GET", "POST"])
def post():

    print('Post..')
    print(request.method)
    if request.method == 'POST':
        print(request.files)
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files.get('image')
        if not file:
            return

        print('file..')

        img_bytes = file.read()

        names, rows = prediction(img_bytes, file.filename.split('.')[0])

        return render_template("index.html", picture=f"./static/{file.filename.split('.')[0]}.jpg",
                               rows=rows)
    return render_template("index.html")


@app.route('/download/<path:filename>')
def download_image(filename):
    return send_file(filename, as_attachment=True)
