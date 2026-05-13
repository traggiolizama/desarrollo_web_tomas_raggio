from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import uuid
from database import db
from validation import validar_formulario

UPLOAD_FOLDER = os.path.join("static", "uploads")

app = Flask(__name__)
app.secret_key = "clave_secreta_dcc"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 32 * 1000 * 1000  


@app.route("/")
def portada():
    ultimos = db.get_ultimos_miembros(5)
    return render_template("portada.html", ultimos=ultimos)


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "GET":
        return render_template("registro.html", errores={}, form={})
    print(request.form)
    archivo = request.files.get("archivo-actividad")
    errores = validar_formulario(request.form, archivo)

    if errores:
        return render_template("registro.html", errores=errores, form=request.form)

   
    miembro_id = db.crear_miembro(
        nombre   = request.form.get("nombre").strip(),
        apellido = request.form.get("apellido").strip(),
        email    = request.form.get("email").strip(),
        telefono = request.form.get("telefono", "").strip(),
        tipo     = request.form.get("tipo-miembro")
    )

  
    extension    = secure_filename(archivo.filename).rsplit(".", 1)[-1].lower()
    nombre_unico = f"{uuid.uuid4()}.{extension}"
    archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], nombre_unico))

   
    dias_marcados = request.form.getlist("dias")
    for dia in dias_marcados:
        actividad_id = db.crear_actividad(
            miembro_id  = miembro_id,
            tipo        = request.form.get("tipo-actividad"),
            nombre      = request.form.get("nombre-actividad").strip(),
            descripcion = request.form.get("descripcion-actividad", "").strip(),
            dia         = dia,
            hora_inicio = request.form.get(f"inicio-{dia}"),
            hora_fin    = request.form.get(f"fin-{dia}"),
            enlace      = request.form.get("enlace-actividad", "").strip()
        )
        db.crear_foto(
            actividad_id   = actividad_id,
            ruta_archivo   = nombre_unico,
            nombre_archivo = secure_filename(archivo.filename)
        )

    return redirect(url_for("portada"))


FILAS_POR_PAGINA = 5

@app.route("/listado")
def listado():
    filtro_tipo = request.args.get("filtro_tipo", "")
    ordenar_por = request.args.get("ordenar_por", "")
    pagina      = request.args.get("pagina", 1, type=int)

    todos     = db.get_todos_miembros(filtro_tipo=filtro_tipo, ordenar_por=ordenar_por)
    total     = len(todos)
    total_pag = max(1, -(-total // FILAS_POR_PAGINA))

    if pagina < 1:
        pagina = 1
    if pagina > total_pag:
        pagina = total_pag

    inicio   = (pagina - 1) * FILAS_POR_PAGINA
    fin      = inicio + FILAS_POR_PAGINA
    miembros = todos[inicio:fin]

    return render_template("listado.html",
        miembros    = miembros,
        pagina      = pagina,
        total_pag   = total_pag,
        filtro_tipo = filtro_tipo,
        ordenar_por = ordenar_por
    )

@app.route("/miembro/<int:id>")
def detalle_miembro(id):
    miembro = db.get_miembro_por_id(id)
    if miembro is None:
        return redirect(url_for("listado"))

    actividades         = db.get_actividades_por_miembro(id)
    fotos_por_actividad = {}
    for actividad in actividades:
        fotos_por_actividad[actividad.id] = db.get_fotos_por_actividad(actividad.id)

    return render_template("detalle.html",
        miembro             = miembro,
        actividades         = actividades,
        fotos_por_actividad = fotos_por_actividad
    )


if __name__ == "__main__":
    app.run(debug=True)