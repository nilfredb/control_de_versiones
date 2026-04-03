from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"

usuarios = []
contador_id = 1


@app.route("/")
def index():
    return render_template("index.html", usuarios=usuarios)


@app.route("/crear", methods=["POST"])
def crear():
    global contador_id
    nombre = request.form.get("nombre", "").strip()
    correo = request.form.get("correo", "").strip()

    if not nombre or not correo:
        flash("Nombre y correo son obligatorios.")
        return redirect(url_for("index"))

    correo_ya_existe = any(u["correo"].lower() == correo.lower() for u in usuarios)
    if correo_ya_existe:
        flash("Ese correo ya está registrado.")
        return redirect(url_for("index"))

    usuarios.append({
        "id": contador_id,
        "nombre": nombre,
        "correo": correo
    })
    contador_id += 1

    flash("Usuario creado correctamente.")
    return redirect(url_for("index"))


@app.route("/eliminar/<int:id>")
def eliminar(id):
    global usuarios
    usuarios = [u for u in usuarios if u["id"] != id]
    flash("Usuario eliminado correctamente.")
    return redirect(url_for("index"))


@app.route("/editar/<int:id>", methods=["POST"])
def editar(id):
    nombre = request.form.get("nombre", "").strip()
    correo = request.form.get("correo", "").strip()

    if not nombre or not correo:
        flash("Nombre y correo son obligatorios para editar.")
        return redirect(url_for("index"))

    for usuario in usuarios:
        if usuario["id"] == id:
            usuario["nombre"] = nombre
            usuario["correo"] = correo
            break

    flash("Usuario editado correctamente.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)