import re
import os

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "mp4", "mov"}
ALLOWED_MIMETYPES  = {"image/jpeg", "image/png", "image/gif", "video/mp4", "video/quicktime"}

TIPOS_MIEMBRO    = {"pregrado", "postgrado", "funcionario", "academico"}
TIPOS_ACTIVIDAD  = {"deportiva", "artistica", "tecnologica", "social", "recreativa"}
DIAS_SEMANA      = {"lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"}


def validar_nombre(valor):
    return len(valor.strip()) >= 3


def validar_apellido(valor):
    return len(valor.strip()) >= 3


def validar_email(valor):
    patron = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return bool(re.match(patron, valor.strip()))


def validar_telefono(valor):
    if not valor or valor.strip() == "":
        return True
    patron = r'^\+?[0-9]{7,15}$'
    return bool(re.match(patron, valor.strip()))


def validar_tipo_miembro(valor):
    return valor in TIPOS_MIEMBRO


def validar_tipo_actividad(valor):
    return valor in TIPOS_ACTIVIDAD


def validar_nombre_actividad(valor):
    return len(valor.strip()) > 0


def validar_dia(valor):
    return valor in DIAS_SEMANA


def validar_hora(valor):
    if not isinstance(valor, str):
        return False
    patron = r'^([01]\d|2[0-3]):[0-5]\d$'
    return bool(re.match(patron, valor.strip()))


def validar_horas(hora_inicio, hora_fin):
    if not validar_hora(hora_inicio) or not validar_hora(hora_fin):
        return False
    return hora_fin > hora_inicio


def validar_enlace(valor):
    if not isinstance(valor, str):
        return False
    patron = r'^https?://.+\..+'
    return bool(re.match(patron, valor.strip()))


def validar_archivo(archivo):
    if archivo is None or archivo.filename == "":
        return False

    extension = archivo.filename.rsplit(".", 1)[-1].lower() if "." in archivo.filename else ""
    if extension not in ALLOWED_EXTENSIONS:
        return False

    mimetype = archivo.mimetype
    if mimetype not in ALLOWED_MIMETYPES:
        return False

    return True

def validar_formulario(form, archivo):
    errores = {}

    if not validar_nombre(form.get("nombre", "")):
        errores["nombre"] = "El nombre debe tener al menos 3 letras."

    if not validar_apellido(form.get("apellido", "")):
        errores["apellido"] = "El apellido debe tener al menos 3 letras."

    if not validar_email(form.get("email", "")):
        errores["email"] = "Ingrese un correo electrónico válido."

    if not validar_telefono(form.get("telefono", "")):
        errores["telefono"] = "Ingrese un número de teléfono válido. Ej: +56912345678"

    if not validar_tipo_miembro(form.get("tipo-miembro", "")):
        errores["tipo-miembro"] = "Seleccione un tipo de miembro válido."

    if not validar_tipo_actividad(form.get("tipo-actividad", "")):
        errores["tipo-actividad"] = "Seleccione un tipo de actividad válido."
    print("antes de validar nombre actividad")
    if not validar_nombre_actividad(form.get("nombre-actividad", "")):
        errores["nombre-actividad"] = "Ingrese el nombre de la actividad."
    print("después de validar nombre actividad, errores:", errores)

    dias_marcados = form.getlist("dias")
    if not dias_marcados:
        errores["dias"] = "Seleccione al menos un día."
    else:
        for dia in dias_marcados:
            if not validar_dia(dia):
                errores["dias"] = "Día inválido."
                break
            hora_inicio = form.get(f"inicio-{dia}", "")
            hora_fin    = form.get(f"fin-{dia}", "")
            if not validar_horas(hora_inicio, hora_fin):
                errores[f"horas-{dia}"] = "Ingrese horas válidas. La hora de término debe ser posterior a la de inicio."

    if not validar_enlace(form.get("enlace-actividad", "")):
        errores["enlace-actividad"] = "Ingrese un enlace válido. Ej: https://instagram.com/mi_club"

    if not validar_archivo(archivo):
        errores["archivo-actividad"] = "Adjunte al menos una foto o video válido (JPG, PNG, GIF, MP4, MOV)."

    return errores


def validar_comentario(nombre, texto):
    errores = {}

    nombre = nombre.strip() if isinstance(nombre, str) else ""
    texto = texto.strip() if isinstance(texto, str) else ""

    if len(nombre) < 3 or len(nombre) > 80:
        errores["nombre"] = "El nombre debe tener entre 3 y 80 caracteres."

    if len(texto) < 5:
        errores["texto"] = "El comentario debe tener al menos 5 caracteres."
    elif len(texto) > 300:
        errores["texto"] = "El comentario no puede superar 300 caracteres."

    return errores
