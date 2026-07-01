package cl.uchile.dcc.tarea4.controller;

import cl.uchile.dcc.tarea4.model.ActividadResultado;
import cl.uchile.dcc.tarea4.model.NotaRequest;
import cl.uchile.dcc.tarea4.model.NotaResponse;
import cl.uchile.dcc.tarea4.service.ActividadService;
import jakarta.persistence.EntityNotFoundException;
import jakarta.validation.Valid;
import java.util.List;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/actividades")
public class ActividadApiController {

    private final ActividadService actividadService;

    public ActividadApiController(ActividadService actividadService) {
        this.actividadService = actividadService;
    }

    @GetMapping("/buscar")
    public List<ActividadResultado> buscar(@RequestParam(name = "q", defaultValue = "") String texto) {
        return actividadService.buscar(texto);
    }

    @PostMapping("/{actividadId}/notas")
    public ResponseEntity<NotaResponse> evaluar(
            @PathVariable Integer actividadId,
            @Valid @RequestBody NotaRequest request
    ) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(actividadService.evaluar(actividadId, request.getNota()));
    }

    @ExceptionHandler(EntityNotFoundException.class)
    public ResponseEntity<Map<String, String>> noEncontrado(EntityNotFoundException exception) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(Map.of("error", exception.getMessage()));
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, String>> validacion(MethodArgumentNotValidException exception) {
        FieldError error = exception.getBindingResult().getFieldErrors().stream().findFirst().orElse(null);
        String mensaje = error == null ? "Datos invalidos." : error.getDefaultMessage();
        return ResponseEntity.badRequest().body(Map.of("error", mensaje));
    }
}
