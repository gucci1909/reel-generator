from flask import Flask, render_template, request
import uuid
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    myid = uuid.uuid1()
    if (request.method == "POST"):
        print(request.files.keys())
        recorded_id = request.form.get("uuid")
        description = request.form.get("text")
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], recorded_id)
        for key, value in request.files.items():
            print(key, value)
            # upload files here
            file = request.files[key]
            if file:
                filename = secure_filename(file.filename)
                os.makedirs(folder_path, exist_ok=True)
                file.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], recorded_id, filename))

            with open(os.path.join(app.config["UPLOAD_FOLDER"], recorded_id, "description.txt"), "w") as f:
                f.write(description)

    return render_template("create.html", myid=myid)

@app.route("/gallery")
def gallery():
    return render_template("gallery.html");


app.run(debug=True)
