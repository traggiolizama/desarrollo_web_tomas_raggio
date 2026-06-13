from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from database import db
from validation import validar_formulario, validar_comentario

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

app = Flask(__name__)
app.secret_key = "clave_secreta_dcc"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 32 * 1000 * 1000  
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


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
    region_id = request.form.get("region", type=int)
    comuna_id = request.form.get("comuna", type=int)

    if region_id is None:
        errores["region"] = "Seleccione una region."

    if comuna_id is None:
        errores["comuna"] = "Seleccione una comuna."
    elif region_id is not None and not db.comuna_pertenece_a_region(comuna_id, region_id):
        errores["comuna"] = "Seleccione una comuna valida para la region indicada."

    if errores:
        return render_template("registro.html", errores=errores, form=request.form)

    nombre_archivo_original = secure_filename(archivo.filename)
    extension = nombre_archivo_original.rsplit(".", 1)[-1].lower()
    nombre_unico = f"{uuid.uuid4()}.{extension}"
    archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], nombre_unico))

    miembro_id = db.crear_miembro(
        nombre   = request.form.get("nombre").strip(),
        apellido = request.form.get("apellido").strip(),
        email    = request.form.get("email").strip(),
        telefono = request.form.get("telefono", "").strip(),
        tipo     = request.form.get("tipo-miembro"),
        comuna_id = comuna_id
    )

   
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
            nombre_archivo = nombre_archivo_original
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


@app.route("/estadisticas")
def estadisticas():
    return render_template("estadísticas.html")


@app.route("/api/estadisticas")
def api_estadisticas():
    return jsonify(db.get_estadisticas())


@app.route("/api/regiones")
def api_regiones():
    return jsonify({
        "ok": True,
        "regiones": db.get_regiones()
    })


@app.route("/api/regiones/<int:region_id>/comunas")
def api_comunas(region_id):
    return jsonify({
        "ok": True,
        "comunas": db.get_comunas_por_region(region_id)
    })


@app.route("/api/actividades/<int:actividad_id>/comentarios", methods=["GET", "POST"])
def comentarios_actividad(actividad_id):
    actividad = db.get_actividad_por_id(actividad_id)
    if actividad is None:
        return jsonify({
            "ok": False,
            "errores": {"general": "La actividad solicitada no existe."}
        }), 404

    if request.method == "GET":
        return jsonify({
            "ok": True,
            "comentarios": db.get_comentarios_por_actividad(actividad_id)
        })

    datos = request.get_json(silent=True) or request.form
    nombre = datos.get("nombre", "")
    texto_comentario = datos.get("texto", "")
    errores = validar_comentario(nombre, texto_comentario)

    if errores:
        return jsonify({
            "ok": False,
            "errores": errores
        }), 400

    comentario = db.crear_comentario(
        actividad_id = actividad_id,
        nombre       = nombre.strip(),
        texto_comentario = texto_comentario.strip()
    )

    return jsonify({
        "ok": True,
        "comentario": comentario
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
