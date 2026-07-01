# Tarea 4 - Aplicacion Spring Boot

Implementacion en Spring Boot de las funcionalidades solicitadas para la Tarea 4 del proyecto de actividades extraprogramaticas del DCC.

Esta aplicacion usa la misma base de datos MySQL de las tareas anteriores (`tarea2.sql`) y agrega una interfaz de busqueda asincrona de actividades, junto con la posibilidad de evaluar actividades mediante notas entre 1 y 7.

## Tecnologias utilizadas

- Java 17 o superior.
- Spring Boot.
- Spring Web.
- Spring Data JPA.
- Thymeleaf.
- MySQL Driver.
- Validation.
- JavaScript en el cliente usando `fetch`.

## Como ejecutar

Desde esta carpeta:

```powershell
cd "spring_app\tarea4"
.\mvnw.cmd spring-boot:run
```

Luego abrir en el navegador:

```text
http://localhost:8080/buscador
```

## Base de datos

La aplicacion espera que exista la base `tarea2`, reutilizando las tablas de las tareas anteriores:

- `region`
- `comuna`
- `miembro`
- `actividad`
- `foto`
- `comentario`

Para esta tarea se agrega la tabla:

- `nota`

```sql
CREATE TABLE IF NOT EXISTS `tarea2`.`nota` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `actividad_id` INT NOT NULL,
  `nota` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_nota_actividad1_idx` (`actividad_id` ASC),
  CONSTRAINT `fk_nota_actividad1`
    FOREIGN KEY (`actividad_id`)
    REFERENCES `tarea2`.`actividad` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
```

## Funcionalidades implementadas

### Buscador de actividades

La vista principal esta en:

```text
/buscador
```

Tambien se puede acceder desde:

```text
/
```

El formulario tiene un unico input de texto. Cuando el usuario escribe al menos 3 caracteres, el navegador realiza una peticion asincrona al backend:

```text
GET /api/actividades/buscar?q=texto
```

La busqueda considera coincidencias en:

- nombre de la actividad;
- descripcion de la actividad;
- nombre de la comuna asociada al miembro de la actividad.

Los resultados muestran:

- nombre completo del miembro;
- dia de la actividad;
- tipo de actividad;
- comuna;
- nombre;
- descripcion;
- nota promedio;
- cantidad de evaluaciones;
- opcion para evaluar.

Si no hay resultados, se muestra un mensaje en la interfaz.

El texto que coincide con el patron buscado se destaca en el navegador usando la etiqueta HTML `mark`. Para evitar interpretar contenido ingresado por usuarios como HTML, el destacado se arma con nodos de texto y no insertando HTML crudo.

### Evaluacion de actividades

Cada resultado incluye un boton `Evaluar`. Al hacer clic, se muestra un selector con notas entre 1 y 7.

Cuando se selecciona una nota, el navegador envia una peticion asincrona:

```text
POST /api/actividades/{actividadId}/notas
```

con cuerpo JSON:

```json
{
  "nota": 6
}
```

El backend valida que la nota sea un numero entero entre 1 y 7 usando anotaciones de validacion:

```java
@NotNull
@Min(1)
@Max(7)
```

Si la nota es valida, se inserta un registro en la tabla `nota`. Despues de guardar, el backend recalcula el promedio y el contador de notas de esa actividad. La interfaz actualiza esos valores sin recargar la pagina.

## Organizacion del codigo

```text
src/main/java/cl/uchile/dcc/tarea4
|-- controller
|   |-- PaginaController.java
|   `-- ActividadApiController.java
|-- model
|   |-- Actividad.java
|   |-- ActividadResultado.java
|   |-- Comuna.java
|   |-- Miembro.java
|   |-- Nota.java
|   |-- NotaRequest.java
|   `-- NotaResponse.java
|-- repository
|   |-- ActividadRepository.java
|   `-- NotaRepository.java
|-- service
|   `-- ActividadService.java
`-- Tarea4Application.java
```

Los modelos `Actividad`, `Miembro`, `Comuna` y `Nota` representan tablas de la base de datos mediante JPA.

Las clases `ActividadResultado`, `NotaRequest` y `NotaResponse` se usan para enviar y recibir datos JSON en la API.

## Decisiones de implementacion

- Se reutiliza la base `tarea2` para mantener los datos existentes de miembros, comunas y actividades.
- La busqueda se hace en el servidor con JPA, y la interfaz se actualiza en el cliente con `fetch`.
- La validacion de notas se hace en cliente y servidor. La validacion del servidor es la principal, porque el cliente puede ser manipulado.
- La nota mostrada corresponde al promedio de todas las notas registradas para una actividad. Si una actividad no tiene notas, se muestra `-`.
- Se muestra un contador de evaluaciones para dejar visible cuantas notas forman el promedio.
- La tabla `nota` no reemplaza datos de `actividad`; cada evaluacion queda como una fila independiente asociada por `actividad_id`.

## Archivos principales del frontend

```text
src/main/resources/templates/buscador.html
src/main/resources/static/js/buscador.js
src/main/resources/static/css/estilos.css
```

El archivo `buscador.js` contiene las llamadas asincronas con `fetch`, el renderizado de resultados, el destacado de coincidencias y la actualizacion de nota/contador despues de evaluar.

## Notas para correccion

- La app Spring Boot de esta tarea se encuentra en `spring_app/tarea4`.
- La app Flask anterior se mantiene en el repositorio como antecedente de las tareas previas y por si se quiere probar hacer la inserción de una actividad para luego evaluarla y probar el funcionamiento de la nueva tarea.
- Para probar la Tarea 4 se debe ejecutar la app Spring Boot, no la app Flask.
