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
@Table(name = "actividad")
public class Actividad {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "miembro_id", nullable = false)
    private Miembro miembro;

    @Column(length = 45, nullable = false)
    private String nombre;

    @Column(columnDefinition = "TEXT")
    private String descripcion;

    @Column(length = 20)
    private String dia;

    @Column(length = 20, nullable = false)
    private String tipo;

    public Integer getId() {
        return id;
    }

    public Miembro getMiembro() {
        return miembro;
    }

    public String getNombre() {
        return nombre;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public String getDia() {
        return dia;
    }

    public String getTipo() {
        return tipo;
    }
}
