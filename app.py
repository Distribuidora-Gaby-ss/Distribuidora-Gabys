from flask import Flask, render_template, request, redirect, url_for, session, flash
import json, os

app = Flask(__name__)
app.secret_key = "distribuidora_gabys_2025"

BASE_DIR = os.path.join(os.path.dirname(__file__), "data")


# ------------------------------
# Ejecutar aplicación
# ------------------------------

if __name__ == "__main__":
    app.run(debug=True)
