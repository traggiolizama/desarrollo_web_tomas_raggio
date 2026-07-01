package cl.uchile.dcc.tarea4.model;

public class NotaResponse {

    private Integer actividadId;
    private String nota;
    private long totalNotas;

    public NotaResponse() {
    }

    public NotaResponse(Integer actividadId, String nota, long totalNotas) {
        this.actividadId = actividadId;
        this.nota = nota;
        this.totalNotas = totalNotas;
    }

    public Integer getActividadId() {
        return actividadId;
    }

    public void setActividadId(Integer actividadId) {
        this.actividadId = actividadId;
    }

    public String getNota() {
        return nota;
    }

    public void setNota(String nota) {
        this.nota = nota;
    }

    public long getTotalNotas() {
        return totalNotas;
    }

    public void setTotalNotas(long totalNotas) {
        this.totalNotas = totalNotas;
    }
}
