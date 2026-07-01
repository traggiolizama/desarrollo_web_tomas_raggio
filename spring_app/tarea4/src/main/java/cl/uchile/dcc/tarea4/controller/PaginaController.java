package cl.uchile.dcc.tarea4.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class PaginaController {

    @GetMapping({"/", "/buscador"})
    public String buscador() {
        return "buscador";
    }
}
