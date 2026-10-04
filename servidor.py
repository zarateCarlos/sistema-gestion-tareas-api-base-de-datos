import sqlite3
from flask import Flask, request, jsonify, redirect
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DB = "usuarios.db"


@app.route("/")
def inicio():
    return redirect("/tareas")


def init_db():
    con = sqlite3.connect(DB)
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL
        )
        """
    )
    con.commit()
    con.close()


@app.route("/registro", methods=["POST"])
def registro():
    data = request.get_json()
    if not data or not data.get("usuario") or not data.get("contraseña"):
        return jsonify({"error": "Faltan datos"}), 400

    usuario = data["usuario"]
    hash_pass = generate_password_hash(data["contraseña"])

    try:
        con = sqlite3.connect(DB)
        con.execute(
            "INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)",
            (usuario, hash_pass),
        )
        con.commit()
        con.close()
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409

    return jsonify({"mensaje": "Usuario registrado correctamente"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("usuario") or not data.get("contraseña"):
        return jsonify({"error": "Faltan datos"}), 400

    con = sqlite3.connect(DB)
    fila = con.execute(
        "SELECT contraseña FROM usuarios WHERE usuario = ?",
        (data["usuario"],),
    ).fetchone()
    con.close()

    if fila is None or not check_password_hash(fila[0], data["contraseña"]):
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

    return jsonify({"mensaje": "Login correcto. Acceso a tareas permitido"}), 200


@app.route("/tareas", methods=["GET"])
def tareas():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Tareas</title>
    </head>
    <body>
        <h1>Bienvenido al Sistema de Gestión de Tareas</h1>
        <p>Sesión iniciada correctamente.</p>
    </body>
    </html>
    """


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
