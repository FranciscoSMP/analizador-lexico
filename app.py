from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from analizador import analizar_codigo

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'clave_secreta_segura'  # Necesario para sesione
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files['file']
        if file and file.filename.endswith(".cpp"):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(filepath)
            with open(filepath, 'r') as f:
                code = f.read()
                tokens = analizar_codigo(code)
            os.remove(filepath)
            
            # Guardar tokens en sesión y redirigir
            session['tokens'] = tokens
            return redirect(url_for('index'))
    
    # Recuperar tokens si existen
    tokens = session.pop('tokens', None)
    return render_template("index.html", tokens=tokens)

if __name__ == "__main__":
    app.run(debug=True)