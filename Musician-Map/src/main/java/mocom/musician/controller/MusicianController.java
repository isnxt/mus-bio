package mocom.musician.controller;

import mocom.musician.service.MusicianService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@Controller
@RequestMapping("/musician")
public class MusicianController {
    @Autowired
    MusicianService musicianService;

    @RequestMapping(method = RequestMethod.GET)
    public String input(Model model) {
        model.addAttribute("musician", musicianService.getMusician());
        model.addAttribute("musicians", musicianService.getAllMusician());
        return "input";
    }

    @RequestMapping(method = RequestMethod.POST)
    public String map(String str, String select, Model model) {
        System.out.println("Str" + str);
        System.out.println("Select" + select);
        if (str == null || str.length() <= 0) {
            if (select.equals("请选择一位音乐家")) {
                model.addAttribute("musician", musicianService.getMusician());
                model.addAttribute("musicians", musicianService.getAllMusician());
                return "input";
            } else {
                musicianService.setMusicians(select);
                model.addAttribute("location", musicianService.getLocation());
                model.addAttribute("desc", musicianService.getDescription());
                return "map";
            }
        } else {
            if (str.equals("Next Page")) {
                model.addAttribute("musician", musicianService.getMusician());
                model.addAttribute("musicians", musicianService.getAllMusician());
                return "input";
            } else {
                musicianService.setMusicians(str);
                model.addAttribute("location", musicianService.getLocation());
                model.addAttribute("desc", musicianService.getDescription());
                return "map";
            }
        }
    }
}
