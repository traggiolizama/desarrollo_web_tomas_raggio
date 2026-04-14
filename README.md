# desarrollo_web_tom-s_raggio
Tarea 1 desarrollo de aplicaciones web
# Actividades DCC

Prototipo de sistema para gestionar las actividades extracurriculares de los miembros del Departamento de Ciencias de la Computación de la Universidad de Chile.

## Archivos del proyecto

- `portada.html`: Página de inicio con acceso a las secciones principales.
- `registro.html`: Formulario de registro de miembros y sus actividades.
- `listado.html`: Listado de miembros con filtro por tipo, ordenamiento y paginación.
- `estadísticas.html`: Visualización de métricas sobre los miembros y actividades.
- `estilos.css`: Hoja de estilos compartida por todas las páginas.
- `validation.js`: Validaciones del formulario de registro.
- `listado.js`: Lógica de filtrado, ordenamiento y paginación del listado.

## Navegación

Todas las páginas incluyen un menú de navegación que permite acceder directamente a cualquier otra sección sin necesidad de volver a la portada.

## Decisiones de diseño

**Formulario de registro**

El formulario está dividido en dos secciones: datos personales y actividad. El único campo opcional es el número de teléfono; todos los demás son obligatorios. Esta decisión se tomó para garantizar que cada miembro registrado tenga la información mínima necesaria para identificarlo y contactarlo en un caso real.

Los errores de validación se muestran en texto rojo debajo de cada campo, y el campo inválido recibe un borde rojo mediante la clase `input-error`. Todas las validaciones están implementadas en JavaScript.

Para los horarios de la actividad, al marcar un día aparecen campos de hora de inicio y término específicos para ese día, permitiendo que una misma actividad se realice en horarios distintos según el día.

**Estadísticas**

La página de estadísticas presenta un gráfico de pastel generado externamente como imagen estática. Se optó por esta solución dado que el enunciado indica que no es necesario almacenar datos reales, por lo que una imagen ilustrativa cumple el objetivo de mostrar la interfaz de métricas del sistema.

**Listado**

Los datos del listado son inventados y están definidos directamente en el archivo `listado.js`. La paginación muestra 5 miembros por página y se actualiza automáticamente al cambiar el filtro o el criterio de ordenamiento.