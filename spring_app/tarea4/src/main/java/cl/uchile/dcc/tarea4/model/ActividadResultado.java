package cl.uchile.dcc.tarea4.model;

public class ActividadResultado {

    private Integer id;
    private String miembro;
    private String dia;
    private String tipo;
    private String comuna;
    private String nombre;
    private String descripcion;
    private String nota;
    private long totalNotas;

    public ActividadResultado() {
    }

    public ActividadResultado(
            Integer id,
            String miembro,
            String dia,
            String tipo,
            String comuna,
            String nombre,
            String descripcion,
            String nota,
            long totalNotas
    ) {
        this.id = id;
        this.miembro = miembro;
        this.dia = dia;
        this.tipo = tipo;
        this.comuna = comuna;
        this.nombre = nombre;
        this.descripcion = descripcion;
        this.nota = nota;
        this.totalNotas = totalNotas;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getMiembro() {
        return miembro;
    }

    public void setMiembro(String miembro) {
        this.miembro = miembro;
    }

    public String getDia() {
        return dia;
    }

    public void setDia(String dia) {
        this.dia = dia;
    }

    public String getTipo() {
        return tipo;
    }

    public void setTipo(String tipo) {
        this.tipo = tipo;
    }

    public String getComuna() {
        return comuna;
    }

    public void setComuna(String comuna) {
        this.comuna = comuna;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public void setDescripcion(String descripcion) {
        this.descripcion = descripcion;
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
