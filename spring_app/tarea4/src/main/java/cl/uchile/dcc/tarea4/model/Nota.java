package cl.uchile.dcc.tarea4.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "nota")
public class Nota {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "actividad_id", nullable = false)
    private Actividad actividad;

    @Column(nullable = false)
    private Integer nota;

    protected Nota() {
    }

    public Nota(Actividad actividad, Integer nota) {
        this.actividad = actividad;
        this.nota = nota;
    }

    public Integer getId() {
        return id;
    }

    public Actividad getActividad() {
        return actividad;
    }

    public Integer getNota() {
        return nota;
    }
}
