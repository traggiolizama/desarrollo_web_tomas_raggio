package cl.uchile.dcc.tarea4.repository;

import cl.uchile.dcc.tarea4.model.Actividad;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface ActividadRepository extends JpaRepository<Actividad, Integer> {

    @Query("""
            select distinct a
            from Actividad a
            join fetch a.miembro m
            left join fetch m.comuna c
            where lower(a.nombre) like lower(concat('%', :texto, '%'))
               or lower(coalesce(a.descripcion, '')) like lower(concat('%', :texto, '%'))
               or lower(coalesce(c.nombre, '')) like lower(concat('%', :texto, '%'))
            order by a.nombre asc
            """)
    List<Actividad> buscarPorTexto(@Param("texto") String texto);
}
