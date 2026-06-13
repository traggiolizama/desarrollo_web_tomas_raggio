# Actividades DCC - Tarea 3

Implementacion del sistema de registro y visualizacion de actividades del DCC usando Flask, SQLAlchemy y MySQL.

Esta entrega extiende la Tarea 2 con estadisticas generadas en el cliente y comentarios asincronos asociados a cada actividad.

## Estructura principal

```text
flask_app/
|-- app.py
|-- database/
|   |-- db.py
|   |-- init_db.py
|   |-- region-comuna.sql
|   `-- tarea2.sql
|-- validation.py
|-- templates/
|   |-- base.html
|   |-- portada.html
|   |-- registro.html
|   |-- listado.html
|   |-- detalle.html
|   `-- template de estadisticas
|-- static/
|   |-- css/estilos.css
|   |-- js/validation.js
|   |-- js/comentarios.js
|   |-- js/estadisticas.js
|   `-- uploads/
`-- requirements.txt
```

## Base de datos

Se usa la base `tarea2` con las tablas de la entrega anterior y la nueva tabla `comentario`.

Para una instalacion desde cero se deben considerar estos scripts:

1. `flask_app/database/tarea2.sql`: estructura inicial de la base.
2. `flask_app/database/region-comuna.sql`: datos de regiones y comunas.
3. `tarea3/tabla-comentario.sql`: tabla de comentarios.

El modelo SQLAlchemy fue extendido con:

- `Region`
- `Comuna`
- `Comentario`
- `Miembro.comuna_id`

Los miembros antiguos que no tienen comuna se mantienen validos. En el grafico por comuna sus actividades se agrupan bajo la etiqueta `Sin comuna`.

## Estadisticas

La pantalla `/estadisticas` muestra tres graficos:

- Lineas: miembros registrados por dia.
- Torta: actividades por tipo.
- Barras: actividades por comuna.

Los graficos se generan en el navegador usando Highcharts. Los datos no se escriben directamente en el HTML: se piden con `fetch` al endpoint:

```text
/api/estadisticas
```

Ese endpoint obtiene los datos desde MySQL usando SQLAlchemy y retorna JSON.

Highcharts se carga desde CDN:

```html
https://code.highcharts.com/highcharts.js
https://code.highcharts.com/modules/accessibility.js
```

Por eso, para ver los graficos con Highcharts, el navegador debe poder cargar esos archivos externos.

## Registro con region y comuna

El formulario de registro ahora incluye seleccion de region y comuna.

El flujo es:

1. `validation.js` carga las regiones con `fetch("/api/regiones")`.
2. Al seleccionar una region, carga sus comunas con `fetch("/api/regiones/<region_id>/comunas")`.
3. En cliente se valida que region y comuna esten seleccionadas.
4. En servidor se valida nuevamente que la comuna exista y pertenezca a la region recibida.
5. Se guarda `comuna_id` en la tabla `miembro`.

Esto permite que los nuevos registros alimenten correctamente el grafico de actividades por comuna.

## Comentarios

En el detalle de cada miembro, cada actividad muestra:

- listado de comentarios existentes;
- formulario para agregar comentario;
- validacion en cliente;
- validacion en servidor;
- insercion en la tabla `comentario`.

Los comentarios se manejan con `fetch` contra:

```text
/api/actividades/<actividad_id>/comentarios
```

Ese endpoint acepta:

- `GET`: lista los comentarios de la actividad.
- `POST`: valida e inserta un nuevo comentario.

Validaciones aplicadas:

- Nombre del comentarista: obligatorio, minimo 3 y maximo 80 caracteres.
- Texto del comentario: obligatorio, minimo 5 caracteres y maximo 300 por el limite de la columna `VARCHAR(300)`.

El contenido escrito por usuarios se muestra con `innerText`, no con `innerHTML`, para evitar que texto malicioso sea interpretado como HTML.

## Validaciones y seguridad

Se mantiene validacion en dos capas:

- Cliente: `static/js/validation.js` y `static/js/comentarios.js`.
- Servidor: `validation.py`.

La validacion del servidor es la mas importante, porque un usuario puede saltarse JavaScript o enviar peticiones manuales.

Los archivos subidos se renombran con UUID y se guardan en `static/uploads/`, evitando colisiones y nombres peligrosos.

## Decisiones de implementacion

Cuando el usuario marca varios dias para una actividad, se inserta una fila en `actividad` por cada dia marcado. Todas quedan asociadas al mismo miembro y comparten la misma foto/video.

Para las estadisticas se separo la responsabilidad:

- Flask consulta la base y entrega JSON.
- JavaScript consume el JSON con `fetch`.
- Highcharts renderiza los graficos en el cliente.

Para comentarios se uso el mismo criterio asincrono:

- La pagina no se recarga al agregar un comentario.
- El formulario queda visible si hay errores.
- El listado se vuelve a cargar despues de una insercion exitosa.

## Como correr la aplicacion

Desde la carpeta `flask_app`:

```bash
venv/Scripts/python.exe app.py
```

Luego abrir:

```text
http://127.0.0.1:5000
```

## Notas para correccion

- Los registros creados antes de agregar region/comuna pueden aparecer como `Sin comuna` en estadisticas.
- La tabla `comentario` debe existir antes de probar comentarios.
- Las tablas `region` y `comuna` deben estar pobladas antes de probar el selector dinamico de region/comuna.
- Los graficos dependen de Highcharts cargado desde CDN.
