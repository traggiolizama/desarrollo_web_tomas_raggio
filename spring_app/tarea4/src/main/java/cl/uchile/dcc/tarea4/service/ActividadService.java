package cl.uchile.dcc.tarea4.service;

import cl.uchile.dcc.tarea4.model.Actividad;
import cl.uchile.dcc.tarea4.model.ActividadResultado;
import cl.uchile.dcc.tarea4.model.Comuna;
import cl.uchile.dcc.tarea4.model.Miembro;
import cl.uchile.dcc.tarea4.model.Nota;
import cl.uchile.dcc.tarea4.model.NotaResponse;
import cl.uchile.dcc.tarea4.repository.ActividadRepository;
import cl.uchile.dcc.tarea4.repository.NotaRepository;
import jakarta.persistence.EntityNotFoundException;
import java.util.List;
import java.util.Locale;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class ActividadService {

    private final ActividadRepository actividadRepository;
    private final NotaRepository notaRepository;

    public ActividadService(ActividadRepository actividadRepository, NotaRepository notaRepository) {
        this.actividadRepository = actividadRepository;
        this.notaRepository = notaRepository;
    }

    @Transactional(readOnly = true)
    public List<ActividadResultado> buscar(String texto) {
        String patron = texto == null ? "" : texto.trim();
        if (patron.length() < 3) {
            return List.of();
        }
        return actividadRepository.buscarPorTexto(patron)
                .stream()
                .map(this::aResultado)
                .toList();
    }

    @Transactional
    public NotaResponse evaluar(Integer actividadId, Integer valorNota) {
        Actividad actividad = actividadRepository.findById(actividadId)
                .orElseThrow(() -> new EntityNotFoundException("La actividad solicitada no existe."));

        notaRepository.save(new Nota(actividad, valorNota));
        return resumenNota(actividadId);
    }

    @Transactional(readOnly = true)
    public NotaResponse resumenNota(Integer actividadId) {
        return new NotaResponse(
                actividadId,
                formatearNota(notaRepository.calcularPromedio(actividadId)),
                notaRepository.countByActividad_Id(actividadId)
        );
    }

    private ActividadResultado aResultado(Actividad actividad) {
        Miembro miembro = actividad.getMiembro();
        Comuna comuna = miembro.getComuna();
        NotaResponse nota = resumenNota(actividad.getId());

        return new ActividadResultado(
                actividad.getId(),
                miembro.getNombreCompleto(),
                texto(actividad.getDia()),
                texto(actividad.getTipo()),
                comuna == null ? "Sin comuna" : comuna.getNombre(),
                texto(actividad.getNombre()),
                texto(actividad.getDescripcion()),
                nota.getNota(),
                nota.getTotalNotas()
        );
    }

    private String formatearNota(Double promedio) {
        if (promedio == null) {
            return "-";
        }
        return String.format(Locale.US, "%.1f", promedio);
    }

    private String texto(String valor) {
        return valor == null ? "" : valor;
    }
}
