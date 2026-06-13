const limpiarErroresComentario = (form) => {
  form.querySelectorAll("[data-error]").forEach((error) => {
    error.innerText = "";
  });

  form.querySelectorAll(".input-error").forEach((input) => {
    input.classList.remove("input-error");
  });
}

const mostrarErroresComentario = (form, errores) => {
  Object.entries(errores).forEach(([campo, mensaje]) => {
    const error = form.querySelector("[data-error='" + campo + "']");
    if (error) {
      error.innerText = mensaje;
    }

    const input = form.elements[campo];
    if (input) {
      input.classList.add("input-error");
    }
  });
}

const validarComentario = (form) => {
  const nombre = form.elements["nombre"];
  const texto = form.elements["texto"];
  const errores = {};

  if (nombre.value.trim().length < 3 || nombre.value.trim().length > 80) {
    errores["nombre"] = "El nombre debe tener entre 3 y 80 caracteres.";
  }

  if (texto.value.trim().length < 5) {
    errores["texto"] = "El comentario debe tener al menos 5 caracteres.";
  } else if (texto.value.trim().length > 300) {
    errores["texto"] = "El comentario no puede superar 300 caracteres.";
  }

  if (Object.keys(errores).length > 0) {
    mostrarErroresComentario(form, errores);
    return false;
  }

  return true;
}

const crearComentarioHTML = (comentario) => {
  const item = document.createElement("article");
  item.classList.add("comentario-item");

  const meta = document.createElement("p");
  meta.classList.add("comentario-meta");
  meta.innerText = comentario.fecha + " - " + comentario.nombre;

  const texto = document.createElement("p");
  texto.innerText = comentario.texto;

  item.appendChild(meta);
  item.appendChild(texto);
  return item;
}

const mostrarComentarios = (section, comentarios) => {
  const lista = section.querySelector(".comentarios-lista");
  lista.innerHTML = "";

  if (comentarios.length === 0) {
    const mensaje = document.createElement("p");
    mensaje.innerText = "Esta actividad todavia no tiene comentarios.";
    lista.appendChild(mensaje);
    return;
  }

  comentarios.forEach((comentario) => {
    lista.appendChild(crearComentarioHTML(comentario));
  });
}

const cargarComentarios = async (section) => {
  const lista = section.querySelector(".comentarios-lista");
  lista.innerHTML = "";

  const mensaje = document.createElement("p");
  mensaje.innerText = "Cargando comentarios...";
  lista.appendChild(mensaje);

  try {
    const respuesta = await fetch(section.dataset.comentariosUrl);
    const datos = await respuesta.json();

    if (!respuesta.ok || !datos.ok) {
      throw new Error("No fue posible cargar los comentarios.");
    }

    mostrarComentarios(section, datos.comentarios);
  } catch (error) {
    lista.innerHTML = "";
    const mensajeError = document.createElement("p");
    mensajeError.classList.add("error");
    mensajeError.innerText = "No fue posible cargar los comentarios.";
    lista.appendChild(mensajeError);
  }
}

const enviarComentario = async (event, section) => {
  event.preventDefault();

  const form = event.currentTarget;
  limpiarErroresComentario(form);

  if (!validarComentario(form)) {
    return;
  }

  const datosComentario = {
    nombre: form.elements["nombre"].value.trim(),
    texto: form.elements["texto"].value.trim()
  };

  try {
    const respuesta = await fetch(section.dataset.comentariosUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(datosComentario)
    });
    const datos = await respuesta.json();

    if (!respuesta.ok || !datos.ok) {
      mostrarErroresComentario(form, datos.errores || {
        general: "No fue posible agregar el comentario."
      });
      return;
    }

    form.reset();
    await cargarComentarios(section);
  } catch (error) {
    mostrarErroresComentario(form, {
      general: "No fue posible agregar el comentario."
    });
  }
}

document.querySelectorAll(".comentarios-actividad").forEach((section) => {
  const form = section.querySelector(".form-comentario");
  form.addEventListener("submit", (event) => enviarComentario(event, section));
  cargarComentarios(section);
});
