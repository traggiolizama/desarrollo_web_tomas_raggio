# desarrollo_web_tom-s_raggio
Tarea 1 desarrollo de aplicaciones web
# Actividades DCC - Tarea 2

Implementación del sistema de gestión de actividades del DCC usando Python con Flask, SQLAlchemy y MySQL.

## Estructura del proyecto

```
flask_app/
├── app.py 
├── database/
│   ├── db.py       # Modelos SQLAlchemy y funciones de base de datos
├── validations.py      # Validaciones del lado del servidor
├── templates/
│   ├── base.html       # Template base con header, main, nav y footer
│   ├── portada.html    # Página de inicio con últimos 5 miembros
│   ├── registro.html   # Formulario de registro
│   ├── listado.html    # Listado de miembros con filtros y paginación
│   └── detalle.html    # Detalle de un miembro y sus actividades
├── static/
│   ├── css/estilos.css
│   ├── js/validation.js
│   └── uploads/        # Archivos subidos por los usuarios
└── venv/
```

## Adaptaciones al modelo de datos

El modelo de datos propuesto fue adaptado para que calzara con las decisiones tomadas en la Tarea 1:

- Se agregó la columna `apellido` a la tabla `miembro`.
- Se agregó la columna `tipo` a la tabla `miembro` con los valores `pregrado`, `postgrado`, `funcionario` y `academico`.
- Se modificó la columna `duracion` de la tabla `actividad` por `hora_fin`, ya que el formulario de la Tarea 1 pedía hora de inicio y hora de término en vez de duración.
- Se agregó la columna `enlace` a la tabla `actividad` para almacenar el enlace a contenido externo de la actividad.
- Se modificaron algunos valores de ENUM para que calzaran con los name puestos en los templates.
- La columna `comuna_id` de la tabla `miembro` se dejó como NULL ya que el formulario de la Tarea 1 no incluía selección de comuna y esta tarea tampoco lo pedía.

## Decisiones de implementación

**Inserción de actividades por día**

Cuando el usuario marca varios días en el formulario, se inserta una fila en la tabla `actividad` por cada día marcado, todas asociadas al mismo miembro. Esto permite almacenar horarios distintos para cada día. El archivo subido se guarda una sola vez y se referencia desde cada fila de la tabla `foto`.

**Validación en dos capas**

El formulario de registro tiene validación en dos capas. Primero `validation.js` valida en el cliente antes de enviar el formulario, dando feedback inmediato al usuario. Luego `validations.py` valida nuevamente en el servidor antes de insertar en la base de datos, lo que protege contra envíos maliciosos que eviten el JS.

**Nombres de archivos subidos**

Los archivos subidos por los usuarios se renombran con un UUID aleatorio antes de guardarse en `static/uploads/`. Esto evita colisiones entre archivos con el mismo nombre y previene que un usuario suba un archivo con un nombre malicioso como `../app.py`.

**Paginación del listado**

La paginación se implementa en el servidor. los enlaces de paginación siempre incluyen los filtros activos para que no se pierdan al cambiar de página.

**Templates con Jinja2**

Todos los templates heredan de `base.html` usando `{% extends %}`. El formulario de registro repuebla los campos con los valores enviados por el usuario cuando hay errores de validación del servidor, mostrando los mensajes de error junto a cada campo.

## Cómo correr la aplicación

1. Activar el entorno virtual:
```bash
source venv/Scripts/activate
```

2. Correr la aplicación:
```bash
venv/Scripts/python.exe app.py
```

3. Abrir en el navegador:
```
http://127.0.0.1:5000
```
