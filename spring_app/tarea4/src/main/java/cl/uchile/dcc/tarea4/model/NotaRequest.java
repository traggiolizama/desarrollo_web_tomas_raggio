package cl.uchile.dcc.tarea4.model;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;

public class NotaRequest {

    @NotNull(message = "Debe seleccionar una nota.")
    @Min(value = 1, message = "La nota minima es 1.")
    @Max(value = 7, message = "La nota maxima es 7.")
    private Integer nota;

    public NotaRequest() {
    }

    public NotaRequest(Integer nota) {
        this.nota = nota;
    }

    public Integer getNota() {
        return nota;
    }

    public void setNota(Integer nota) {
        this.nota = nota;
    }
}
