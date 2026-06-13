const etiquetasTipoActividad = {
  deportiva: "Deportiva",
  artistica: "Artística",
  tecnologica: "Tecnológica",
  social: "Social",
  recreativa: "Recreativa"
};

const coloresGraficos = [
  "#c0392b",
  "#2874a6",
  "#1e8449",
  "#b9770e",
  "#7d3c98",
  "#117864",
  "#922b21"
];

const mostrarMensajeGrafico = (id, texto) => {
  const mensaje = document.getElementById(id);
  mensaje.innerText = texto;
}

const ocultarMensajeGrafico = (id) => {
  mostrarMensajeGrafico(id, "");
}

const fechaCorta = (fecha) => {
  const fechaLocal = new Date(fecha + "T00:00:00");
  return fechaLocal.toLocaleDateString("es-CL", {
    day: "2-digit",
    month: "2-digit"
  });
}

const mostrarSinDatos = (contenedorId, mensajeId, texto) => {
  document.getElementById(contenedorId).innerHTML = "";
  mostrarMensajeGrafico(mensajeId, texto);
}

const dibujarGraficoLineas = (datos) => {
  if (datos.length === 0) {
    mostrarSinDatos("grafico-miembros-dia", "mensaje-miembros-dia", "No hay miembros registrados.");
    return;
  }

  ocultarMensajeGrafico("mensaje-miembros-dia");

  Highcharts.chart("grafico-miembros-dia", {
    chart: {
      type: "line"
    },
    title: {
      text: ""
    },
    credits: {
      enabled: false
    },
    colors: coloresGraficos,
    xAxis: {
      categories: datos.map((item) => fechaCorta(item.fecha)),
      title: {
        text: "Día"
      }
    },
    yAxis: {
      allowDecimals: false,
      min: 0,
      title: {
        text: "Miembros registrados"
      }
    },
    tooltip: {
      pointFormat: "Miembros: <b>{point.y}</b>"
    },
    series: [{
      name: "Miembros",
      data: datos.map((item) => item.total)
    }]
  });
}

const dibujarGraficoTorta = (datos) => {
  if (datos.length === 0) {
    mostrarSinDatos("grafico-actividades-tipo", "mensaje-actividades-tipo", "No hay actividades registradas.");
    return;
  }

  ocultarMensajeGrafico("mensaje-actividades-tipo");

  Highcharts.chart("grafico-actividades-tipo", {
    chart: {
      type: "pie"
    },
    title: {
      text: ""
    },
    credits: {
      enabled: false
    },
    colors: coloresGraficos,
    tooltip: {
      pointFormat: "Total: <b>{point.y}</b>"
    },
    accessibility: {
      point: {
        valueSuffix: " actividades"
      }
    },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: "pointer",
        dataLabels: {
          enabled: true,
          format: "{point.name}: {point.y}"
        },
        showInLegend: true
      }
    },
    series: [{
      name: "Actividades",
      colorByPoint: true,
      data: datos.map((item) => ({
        name: etiquetasTipoActividad[item.tipo] || item.tipo,
        y: item.total
      }))
    }]
  });
}

const dibujarGraficoBarras = (datos) => {
  if (datos.length === 0) {
    mostrarSinDatos("grafico-actividades-comuna", "mensaje-actividades-comuna", "No hay actividades registradas.");
    return;
  }

  ocultarMensajeGrafico("mensaje-actividades-comuna");

  Highcharts.chart("grafico-actividades-comuna", {
    chart: {
      type: "column"
    },
    title: {
      text: ""
    },
    credits: {
      enabled: false
    },
    colors: coloresGraficos,
    xAxis: {
      categories: datos.map((item) => item.comuna),
      title: {
        text: "Comuna"
      }
    },
    yAxis: {
      allowDecimals: false,
      min: 0,
      title: {
        text: "Actividades registradas"
      }
    },
    tooltip: {
      pointFormat: "Actividades: <b>{point.y}</b>"
    },
    series: [{
      name: "Actividades",
      data: datos.map((item) => item.total)
    }]
  });
}

const cargarEstadisticas = async () => {
  if (typeof Highcharts === "undefined") {
    mostrarMensajeGrafico("mensaje-miembros-dia", "No fue posible cargar Highcharts.");
    mostrarMensajeGrafico("mensaje-actividades-tipo", "No fue posible cargar Highcharts.");
    mostrarMensajeGrafico("mensaje-actividades-comuna", "No fue posible cargar Highcharts.");
    return;
  }

  try {
    const respuesta = await fetch("/api/estadisticas");
    const datos = await respuesta.json();

    if (!respuesta.ok) {
      throw new Error("No fue posible obtener las estadísticas.");
    }

    dibujarGraficoLineas(datos.miembros_por_dia);
    dibujarGraficoTorta(datos.actividades_por_tipo);
    dibujarGraficoBarras(datos.actividades_por_comuna);
  } catch (error) {
    mostrarMensajeGrafico("mensaje-miembros-dia", "No fue posible cargar las estadísticas.");
    mostrarMensajeGrafico("mensaje-actividades-tipo", "No fue posible cargar las estadísticas.");
    mostrarMensajeGrafico("mensaje-actividades-comuna", "No fue posible cargar las estadísticas.");
  }
}

cargarEstadisticas();
