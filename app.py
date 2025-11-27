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

def guardar_json(nombre_archivo, data):
    ruta = os.path.join(BASE_DIR, nombre_archivo)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

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


@app.route("/productos")
def productos():
    if "usuario" not in session:
        return redirect(url_for("login"))
    productos = cargar_json("productos.json")
    
    query = request.args.get("q", "").strip().lower()
    tipo_filtro = request.args.get("tipo", "").strip().lower()
    if query or tipo_filtro:
        productos = [
            p for p in productos
            if (not query or query in p["nombre"].lower() or query in p["codigo"].lower())
            and (not tipo_filtro or p["tipo"].lower() == tipo_filtro)
        ]

    return render_template("productos.html", productos=productos)

@app.route("/productos/eliminar/<codigo>", methods=["POST"])
def eliminar_producto(codigo):
    if "usuario" not in session:
        return redirect(url_for("login"))

    productos = cargar_json("productos.json")
    producto = next((p for p in productos if p["codigo"] == codigo), None)

    if not producto:
        flash("Producto no encontrado.", "danger")
    else:
        productos = [p for p in productos if p["codigo"] != codigo]
        guardar_json("productos.json", productos)
        flash(f"Producto '{producto['nombre']}' eliminado correctamente.", "success")

    return redirect(url_for("productos"))

@app.route("/productos/editar/<codigo>", methods=["GET", "POST"])
def editar_producto(codigo):
    if "usuario" not in session:
        return redirect(url_for("login"))

    productos = cargar_json("productos.json")
    producto = next((p for p in productos if p["codigo"] == codigo), None)

    if not producto:
        flash("Producto no encontrado.", "danger")
        return redirect(url_for("productos"))

    tipos = ["aseo personal", "hogar", "otros"]

    if request.method == "POST":
        nuevo_codigo = request.form["codigo"]
        if nuevo_codigo != codigo and any(p["codigo"] == nuevo_codigo for p in productos):
            flash("Ya existe otro producto con ese código.", "danger")
            return redirect(url_for("editar_producto", codigo=codigo))

        producto["nombre"] = request.form["nombre"]
        producto["codigo"] = nuevo_codigo
        producto["cantidad"] = int(request.form["cantidad"])
        producto["precio"] = float(request.form["precio"])
        producto["tipo"] = request.form["tipo"]

        guardar_json("productos.json", productos)
        flash("Producto actualizado correctamente.", "success")
        return redirect(url_for("productos"))

    return render_template("editar_producto.html", producto=producto, tipos=tipos)

# ------------------------------
# Otras secciones
# ------------------------------

@app.route("/alertas")
def alertas():
    if "usuario" not in session:
        return redirect(url_for("login"))
    alertas = cargar_json("alertas.json")
    return render_template("alertas.html", alertas=alertas)



# ------------------------------
# Ejecutar aplicación
# ------------------------------

if __name__ == "__main__":
    app.run(debug=True)

