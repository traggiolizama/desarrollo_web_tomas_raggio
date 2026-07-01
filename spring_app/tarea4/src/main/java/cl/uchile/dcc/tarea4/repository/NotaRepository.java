package cl.uchile.dcc.tarea4.repository;

import cl.uchile.dcc.tarea4.model.Nota;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface NotaRepository extends JpaRepository<Nota, Integer> {

    long countByActividad_Id(Integer actividadId);

    @Query("select avg(n.nota) from Nota n where n.actividad.id = :actividadId")
    Double calcularPromedio(@Param("actividadId") Integer actividadId);
}
