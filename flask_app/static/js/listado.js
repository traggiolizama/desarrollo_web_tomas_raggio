const miembros = [
  { nombre: "Ana",      apellido: "García",    email: "ana.garcia@uchile.cl",    tipo: "pregrado",    actividad: "deportiva"   },
  { nombre: "Carlos",   apellido: "Muñoz",     email: "carlos.munoz@uchile.cl",  tipo: "postgrado",   actividad: "tecnologica" },
  { nombre: "Beatriz",  apellido: "López",     email: "beatriz.lopez@uchile.cl", tipo: "academico",   actividad: "artistica"   },
  { nombre: "Diego",    apellido: "Torres",    email: "diego.torres@uchile.cl",  tipo: "funcionario", actividad: "social"      },
  { nombre: "Elena",    apellido: "Ramírez",   email: "elena.ramirez@uchile.cl", tipo: "pregrado",    actividad: "recreativa"  },
  { nombre: "Felipe",   apellido: "Castro",    email: "felipe.castro@uchile.cl", tipo: "postgrado",   actividad: "deportiva"   },
  { nombre: "Gloria",   apellido: "Herrera",   email: "gloria.herrera@uchile.cl",tipo: "academico",   actividad: "tecnologica" },
  { nombre: "Héctor",   apellido: "Díaz",      email: "hector.diaz@uchile.cl",   tipo: "pregrado",    actividad: "artistica"   },
  { nombre: "Isabel",   apellido: "Vargas",    email: "isabel.vargas@uchile.cl", tipo: "funcionario", actividad: "social"      },
  { nombre: "Javier",   apellido: "Morales",   email: "javier.morales@uchile.cl",tipo: "pregrado",    actividad: "recreativa"  },
  { nombre: "Karen",    apellido: "Soto",      email: "karen.soto@uchile.cl",    tipo: "postgrado",   actividad: "artistica"   },
  { nombre: "Luis",     apellido: "Pizarro",   email: "luis.pizarro@uchile.cl",  tipo: "academico",   actividad: "deportiva"   },
];

const etiquetasTipo = {
  pregrado:    "Estudiante de pregrado",
  postgrado:   "Estudiante de postgrado",
  funcionario: "Funcionario/a",
  academico:   "Académico/a",
};
 
const etiquetasActividad = {
  deportiva:   "Deportiva",
  artistica:   "Artística",
  tecnologica: "Tecnológica",
  social:      "Social",
  recreativa:  "Recreativa",
};

const filas_por_pagina = 5;
let paginaActual = 1;

const datosFiltrados = () => {
    const filtroTipo = document.getElementById("filtro-tipo").value;
    const ordenarPor = document.getElementById("ordenar-por").value;
    
    let datos = miembros.slice();

    if (filtroTipo !== ""){
        datos = datos.filter((m) => {
            return m.tipo === filtroTipo;
        })
    }

    if (ordenarPor !== ""){
        datos.sort((a, b) => {
            return a[ordenarPor].localeCompare(b[ordenarPor]);
        })   
    }
    return datos
}

const construirTabla = () => {
    const datos = datosFiltrados();
    const totalPaginas = Math.ceil(datos.length/ filas_por_pagina);

    if (paginaActual > totalPaginas){
        paginaActual = 1;
    }

    const inicio = (paginaActual-1)*filas_por_pagina;
    const final = inicio + filas_por_pagina;
    const datosPágina = datos.slice(inicio, final);

    const cuerpo = document.getElementById("cuerpo-tabla");
    cuerpo.innerHTML = "";

    datosPágina.forEach((m) => {
        const fila = document.createElement("tr")

        const celdas = [
            m.nombre,
            m.apellido,
            m.email,
            etiquetasTipo[m.tipo],
            etiquetasActividad[m.actividad],
        ]
        
        celdas.forEach((campo) => {
            const celda = document.createElement("td");
            celda.innerText = campo;
            fila.appendChild(celda)
        });

        cuerpo.appendChild(fila)
    });

    document.getElementById("indicador-pagina").innerText = "Página " + paginaActual + " de " + (totalPaginas || 1);

    document.getElementById("btn-anterior").disabled = paginaActual === 1;
    document.getElementById("btn-siguiente").disabled = (paginaActual === totalPaginas) || (totalPaginas === 0);
    
}

document.getElementById("filtro-tipo").addEventListener("change", () => {
    paginaActual = 1;
    construirTabla();
})

document.getElementById("ordenar-por").addEventListener("change", () => {
    paginaActual = 1;
    construirTabla();
})

document.getElementById("btn-anterior").addEventListener("click", () => {
    paginaActual = paginaActual-1;
    construirTabla();
})

document.getElementById("btn-siguiente").addEventListener("click", () => {
    paginaActual = paginaActual+1;
    construirTabla();
})

construirTabla();