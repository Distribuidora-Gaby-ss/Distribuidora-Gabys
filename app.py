from flask import Flask, render_template, request, redirect, url_for, session, flash
import json, os

app = Flask(__name__)
app.secret_key = "distribuidora_gabys_2025"

BASE_DIR = os.path.join(os.path.dirname(__file__), "data")

# ------------------------------
# Funciones auxiliares
# ------------------------------

def cargar_json(nombre_archivo):
    ruta = os.path.join(BASE_DIR, nombre_archivo)
    if not os.path.exists(ruta):
        return []
    with open(ruta, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# ------------------------------
# Rutas principales
# ------------------------------

@app.route("/")
def index():
    if "usuario" in session:
        return redirect(url_for("menu"))
    return redirect(url_for("login"))

@app.route("/menu")
def menu():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", usuario=session["usuario"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuarios = cargar_json("usuarios.json")
        user = request.form["usuario"]
        pwd = request.form["password"]

        for u in usuarios:
            if u["usuario"] == user and u["password"] == pwd:
                session["usuario"] = user
                flash("Inicio de sesión exitoso", "success")
                # Redirige a /menu según lo que espera el test
                return redirect(url_for("menu"))

        # Mensaje exacto esperado por el test
        flash("Credenciales incorrectas", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    session.pop("carrito", None)
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for("login"))

# ------------------------------
# Ejecutar aplicación
# ------------------------------

if __name__ == "__main__":
    app.run(debug=True)

