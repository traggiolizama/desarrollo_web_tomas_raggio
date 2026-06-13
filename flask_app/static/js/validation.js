const validarNombre = () => {
  const input = document.getElementById("nombre");
  const error = document.getElementById("error-nombre");
  const valor = input.value.trim();
 
  if (valor.length < 3) {
    error.innerText = "El nombre debe tener al menos 3 letras.";
    input.classList.add("input-error");
    return false;
  }
 
  error.innerText = "";
  input.classList.remove("input-error");
  return true;
}
 
const validarApellido = () => {
  const input = document.getElementById("apellido");
  const error = document.getElementById("error-apellido");
  const valor = input.value.trim();
 
  if (valor.length < 3) {
    error.innerText = "El apellido debe tener al menos 3 letras.";
    input.classList.add("input-error");
    return false;
  }
 
  error.innerText = "";
  input.classList.remove("input-error");
  return true;
}
 
const validarCorreo = () => {
  const input = document.getElementById("email");
  const error = document.getElementById("error-email");
  const valor = input.value.trim();
  const formatoCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
 
  if (!formatoCorreo.test(valor)) {
    error.innerText = "Ingrese un correo electrónico válido. Ej: tomas.raggio@ug.uchile.cl";
    input.classList.add("input-error");
    return false;
  }
 
  error.innerText = "";
  input.classList.remove("input-error");
  return true;
}
 
const validarTelefono = () =>  {
  const input = document.getElementById("telefono");
  const error = document.getElementById("error-telefono");
  const valor = input.value.trim();
  const formatoTelefono = /^\+?[0-9]{7,15}$/;
 
  if (valor === "") {
    error.innerText = "";
    input.classList.remove("input-error");
    return true;
  }
 
  if (!formatoTelefono.test(valor)) {
    error.innerText = "Ingrese un número de teléfono válido. Ej: +56912345678";
    input.classList.add("input-error");
    return false;
  }
 
  error.innerText = "";
  input.classList.remove("input-error");
  return true;
}
 
const validarTipoMiembro = () => {
  const input = document.getElementById("tipo-miembro");
  const error = document.getElementById("error-tipo-miembro");
 
  if (input.value === "") {
    error.innerText = "Seleccione un tipo de miembro.";
    input.classList.add("input-error");
    return false;
  }
 
  error.innerText = "";
  input.classList.remove("input-error");
  return true;
}

const validarRegion = () => {
  const input = document.getElementById("region");
  const error = document.getElementById("error-region");

  if (input.value === "") {
    error.innerText = "Seleccione una region.";
    input.classList.add("input-error");
    return false;
  }

  error.innerText = "";
  input.classList.remove("input-error");
  return true;
}

const validarComuna = () => {
  const input = document.getElementById("comuna");
  const error = document.getElementById("error-comuna");

  if (input.value === "") {
    error.innerText = "Seleccione una comuna.";
    input.classList.add("input-error");
    return false;
  }

  error.innerText = "";
  input.classList.remove("input-error");
  return true;
}

const validarTipoActividad = () => {
  const input = document.getElementById("tipo-actividad");
  const error = document.getElementById("error-tipo-actividad");
 
  if (input.value === "") {
    error.innerText = "Seleccione un tipo de actividad.";
    input.classList.add("input-error");
    return false;
  }
 
  error.innerText = "";
  input.classList.remove("input-error");
  return true;
}
 

 
const validarDias = () => {
  const checkboxes = document.querySelectorAll("input[name='dias']:checked");
  const error = document.getElementById("error-dias");
 
  if (checkboxes.length === 0) {
    error.innerText = "Seleccione al menos un día.";
    return false;
  }
 
  error.innerText = "";
  return true;
}
 
const validarHorasDia = (dia) => {
  const inicio = document.getElementById("inicio-" + dia);
  const fin = document.getElementById("fin-" + dia);
  const errorHora = document.getElementById("error-hora-" + dia);
  let valido = true;
  console.log("inicio:", inicio.value, "fin:", fin.value);
  if ((inicio.value === "") || (fin.value === "")){
    errorHora.innerText = "Ingrese una hora válida";
    valido = false;
  } else if (fin.value <= inicio.value) {
  errorHora.innerText = "La hora de término debe ser posterior a la de inicio.";
  valido = false; 
    
  } else {
    errorHora.innerText = "";
    fin.classList.remove("input-error");
  }
 
  return valido;
}
 
const validarHorasActividad = () => {
  const dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"];
  let valido = true;
 
  dias.forEach((dia) => {
    const checkbox = document.querySelector("input[name='dias'][value='"+dia+"']");
    if (checkbox && checkbox.checked) {
      if (!validarHorasDia(dia)) {
        valido = false;
      }
    }
  });
 
  return valido;
}
 
const validarArchivo = () => {
  const input = document.getElementById("archivo-actividad");
  const error = document.getElementById("error-archivo");
 
  if (input.files.length === 0) {
    error.innerText = "Adjunte al menos una foto o video de la actividad.";
    return false;
  }
 
  error.innerText = "";
  return true;
}
 
const validarEnlace = () => {
  const input = document.getElementById("enlace-actividad");
  const error = document.getElementById("error-enlace");
  const valor = input.value.trim();
  const formatoUrl = /^https?:\/\/.+\..+/;
 
  if (!formatoUrl.test(valor)) {
    error.innerText = "Ingrese un enlace válido. Ej: https://instagram.com/aaaa";
    input.classList.add("input-error");
    return false;
  }
 
  error.innerText = "";
  input.classList.remove("input-error");
  return true;
}

const validarFormulario = () => {
  let valido = true;
 
  if (!validarNombre())          valido = false;
  if (!validarApellido())        valido = false;
  if (!validarCorreo())          valido = false;
  if (!validarTelefono())        valido = false;
  if (!validarTipoMiembro())     valido = false;
  if (!validarRegion())          valido = false;
  if (!validarComuna())          valido = false;
  if (!validarTipoActividad())   valido = false;
  if (!validarDias())            valido = false;
  if (!validarHorasActividad())  valido = false;
  if (!validarArchivo())         valido = false;
  if (!validarEnlace())          valido = false;
 
  return valido;
}

const agregarOpcion = (select, valor, texto) => {
  const opcion = document.createElement("option");
  opcion.value = valor;
  opcion.innerText = texto;
  select.appendChild(opcion);
}

const limpiarSelectComuna = (texto) => {
  const comuna = document.getElementById("comuna");
  comuna.innerHTML = "";
  agregarOpcion(comuna, "", texto);
  comuna.disabled = true;
}

const cargarComunas = async (regionId, comunaSeleccionada = "") => {
  limpiarSelectComuna("-- Cargando comunas --");

  if (regionId === "") {
    limpiarSelectComuna("-- Seleccione una region --");
    return;
  }

  try {
    const respuesta = await fetch("/api/regiones/" + regionId + "/comunas");
    const datos = await respuesta.json();

    if (!respuesta.ok || !datos.ok) {
      throw new Error("No fue posible cargar las comunas.");
    }

    const comuna = document.getElementById("comuna");
    comuna.innerHTML = "";
    agregarOpcion(comuna, "", "-- Seleccione --");

    datos.comunas.forEach((item) => {
      agregarOpcion(comuna, item.id, item.nombre);
    });

    comuna.disabled = false;

    if (comunaSeleccionada !== "") {
      comuna.value = comunaSeleccionada;
    }
  } catch (error) {
    limpiarSelectComuna("-- No fue posible cargar comunas --");
  }
}

const cargarRegiones = async () => {
  const form = document.getElementById("form-datos");
  const region = document.getElementById("region");
  const regionSeleccionada = form.dataset.regionSeleccionada;
  const comunaSeleccionada = form.dataset.comunaSeleccionada;

  try {
    const respuesta = await fetch("/api/regiones");
    const datos = await respuesta.json();

    if (!respuesta.ok || !datos.ok) {
      throw new Error("No fue posible cargar las regiones.");
    }

    datos.regiones.forEach((item) => {
      agregarOpcion(region, item.id, item.nombre);
    });

    if (regionSeleccionada !== "") {
      region.value = regionSeleccionada;
      await cargarComunas(regionSeleccionada, comunaSeleccionada);
    }
  } catch (error) {
    const errorRegion = document.getElementById("error-region");
    errorRegion.innerText = "No fue posible cargar las regiones.";
  }
}

const checkboxes = document.querySelectorAll("input[name='dias']");
 
checkboxes.forEach((checkbox) => {
  checkbox.addEventListener("change", () => {
    const contenedorHoras = document.getElementById("hora-" + checkbox.value);
    if (checkbox.checked) {
      contenedorHoras.classList.add("visible");
    } else {
      contenedorHoras.classList.remove("visible");
    }
  });
});

document.getElementById("region").addEventListener("change", (event) => {
  document.getElementById("error-region").innerText = "";
  document.getElementById("error-comuna").innerText = "";
  cargarComunas(event.target.value);
});

document.getElementById("btn-enviar").addEventListener("click", (event) => {
  console.log("click recibido");
  const vali = validarFormulario()
  console.log("validación:", vali);
  if (vali) {
    document.getElementById("form-datos").submit();
  };
  
});

cargarRegiones();
