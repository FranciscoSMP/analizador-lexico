from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from analizador import analizar_codigo

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    tokens = []
    if request.method == "POST":
        file = request.files['file']
        if file and file.filename.endswith(".cpp"):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(filepath)
            with open(filepath, 'r') as f:
                code = f.read()
                tokens = analizar_codigo(code)
            os.remove(filepath)
    return render_template("index.html", tokens=tokens)

if __name__ == "__main__":
    app.run(debug=True)
