const inputBusqueda = document.querySelector("#texto-busqueda");
const mensaje = document.querySelector("#mensaje");
const tabla = document.querySelector("#tabla-resultados");
const cuerpo = document.querySelector("#cuerpo-resultados");
const formBusqueda = document.querySelector("#form-busqueda");

let temporizador = null;
let ultimaBusqueda = "";

formBusqueda.addEventListener("submit", (evento) => {
    evento.preventDefault();
    buscar();
});

inputBusqueda.addEventListener("input", () => {
    window.clearTimeout(temporizador);
    temporizador = window.setTimeout(buscar, 250);
});

async function buscar() {
    const texto = inputBusqueda.value.trim();
    ultimaBusqueda = texto;

    if (texto.length < 3) {
        cuerpo.replaceChildren();
        tabla.classList.add("oculto");
        mostrarMensaje("Escribe al menos 3 caracteres para buscar.");
        return;
    }

    mostrarMensaje("Buscando...");

    try {
        const respuesta = await fetch(`/api/actividades/buscar?q=${encodeURIComponent(texto)}`);
        if (!respuesta.ok) {
            throw new Error("No fue posible buscar actividades.");
        }

        const actividades = await respuesta.json();
        if (texto !== ultimaBusqueda) {
            return;
        }

        renderizarResultados(actividades, texto);
    } catch (error) {
        cuerpo.replaceChildren();
        tabla.classList.add("oculto");
        mostrarMensaje(error.message, true);
    }
}

function renderizarResultados(actividades, patron) {
    cuerpo.replaceChildren();

    if (actividades.length === 0) {
        tabla.classList.add("oculto");
        mostrarMensaje("No se encontraron actividades para la busqueda.");
        return;
    }

    for (const actividad of actividades) {
        cuerpo.appendChild(crearFila(actividad, patron));
    }

    tabla.classList.remove("oculto");
    mostrarMensaje(`${actividades.length} resultado(s) encontrado(s).`);
}

function crearFila(actividad, patron) {
    const fila = document.createElement("tr");
    fila.dataset.actividadId = actividad.id;

    agregarCeldaTexto(fila, actividad.miembro);
    agregarCeldaTexto(fila, actividad.dia);
    agregarCeldaTexto(fila, actividad.tipo);
    agregarCeldaDestacada(fila, actividad.comuna, patron);
    agregarCeldaDestacada(fila, actividad.nombre, patron);
    agregarCeldaDestacada(fila, actividad.descripcion, patron, "descripcion");

    const celdaNota = agregarCeldaTexto(fila, actividad.nota, "nota");
    celdaNota.dataset.campo = "nota";

    const celdaTotal = agregarCeldaTexto(fila, String(actividad.totalNotas));
    celdaTotal.dataset.campo = "total";

    const celdaEvaluar = document.createElement("td");
    const boton = document.createElement("button");
    boton.type = "button";
    boton.className = "boton";
    boton.textContent = "Evaluar";
    boton.addEventListener("click", () => pedirNota(celdaEvaluar, actividad.id));
    celdaEvaluar.appendChild(boton);
    fila.appendChild(celdaEvaluar);

    return fila;
}

function agregarCeldaTexto(fila, texto, clase = "") {
    const celda = document.createElement("td");
    if (clase) {
        celda.className = clase;
    }
    celda.textContent = texto || "";
    fila.appendChild(celda);
    return celda;
}

function agregarCeldaDestacada(fila, texto, patron, clase = "") {
    const celda = document.createElement("td");
    if (clase) {
        celda.className = clase;
    }
    agregarTextoDestacado(celda, texto || "", patron);
    fila.appendChild(celda);
}

function agregarTextoDestacado(contenedor, texto, patron) {
    const patronNormalizado = patron.toLowerCase();
    const textoNormalizado = texto.toLowerCase();
    let inicio = 0;
    let indice = textoNormalizado.indexOf(patronNormalizado);

    while (indice !== -1) {
        contenedor.appendChild(document.createTextNode(texto.slice(inicio, indice)));

        const marca = document.createElement("mark");
        marca.textContent = texto.slice(indice, indice + patron.length);
        contenedor.appendChild(marca);

        inicio = indice + patron.length;
        indice = textoNormalizado.indexOf(patronNormalizado, inicio);
    }

    contenedor.appendChild(document.createTextNode(texto.slice(inicio)));
}

function pedirNota(celda, actividadId) {
    if (celda.querySelector("select")) {
        celda.querySelector("select").focus();
        return;
    }

    const selector = document.createElement("select");
    selector.className = "selector-nota";
    selector.setAttribute("aria-label", "Seleccionar nota");

    const opcionBase = document.createElement("option");
    opcionBase.value = "";
    opcionBase.textContent = "Nota";
    selector.appendChild(opcionBase);

    for (let nota = 1; nota <= 7; nota += 1) {
        const opcion = document.createElement("option");
        opcion.value = String(nota);
        opcion.textContent = String(nota);
        selector.appendChild(opcion);
    }

    selector.addEventListener("change", () => evaluarActividad(actividadId, selector));
    celda.appendChild(selector);
    selector.focus();
}

async function evaluarActividad(actividadId, selector) {
    const nota = Number(selector.value);
    if (!Number.isInteger(nota) || nota < 1 || nota > 7) {
        return;
    }

    selector.disabled = true;
    mostrarMensaje("Guardando nota...");

    try {
        const respuesta = await fetch(`/api/actividades/${actividadId}/notas`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ nota })
        });

        const datos = await respuesta.json();
        if (!respuesta.ok) {
            throw new Error(datos.error || "No fue posible guardar la nota.");
        }

        actualizarNota(datos);
        selector.remove();
        mostrarMensaje("Nota guardada correctamente.");
    } catch (error) {
        selector.disabled = false;
        mostrarMensaje(error.message, true);
    }
}

function actualizarNota(datos) {
    const fila = document.querySelector(`tr[data-actividad-id="${datos.actividadId}"]`);
    if (!fila) {
        return;
    }

    fila.querySelector('[data-campo="nota"]').textContent = datos.nota;
    fila.querySelector('[data-campo="total"]').textContent = String(datos.totalNotas);
}

function mostrarMensaje(texto, esError = false) {
    mensaje.textContent = texto;
    mensaje.classList.toggle("error", esError);
}
