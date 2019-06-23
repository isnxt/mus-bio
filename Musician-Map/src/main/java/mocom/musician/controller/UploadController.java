package mocom.musician.controller;

import mocom.musician.entity.Biology;
import mocom.musician.entity.Incident;
import mocom.musician.service.UploadService;
import mocom.musician.util.OperateFile;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestPart;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Controller
@RequestMapping("/upload")
public class UploadController {
    @Autowired
    UploadService uploadService;

    @Autowired
    OperateFile operateFile;

    @RequestMapping(method = RequestMethod.GET)
    public String input() {
        return "upload";
    }

    @RequestMapping(method = RequestMethod.POST)
    public String getTimeLine(@RequestPart("file") MultipartFile file, Biology biology, Model model) {
        if (biology.getStartTime() == null || biology.getEndTime() == null || biology.getMusician() == null || file.isEmpty()) {
            return "redirect:/upload";
        }
        // 获取文件名
        String fileName = file.getOriginalFilename();

        String filePath = System.getProperty("user.dir");
        System.out.println(filePath);
        filePath += "\\src\\main\\resources";
        File dest = new File(filePath + "\\data\\" + fileName);
        String inPath = filePath + "\\data\\" + file.getOriginalFilename();
        System.out.println(dest);
        // 检测是否存在目录
        if (!dest.getParentFile().exists()) {
            dest.getParentFile().mkdirs();
        }
        try {
            file.transferTo(dest);
            System.out.println("上传成功");
        } catch (IOException e) {
            e.printStackTrace();
        }

        String pyPath = "E:\\Software\\Middleware\\Musican\\Musician\NLP-zh";  // python 工程路径
        String outPath = filePath + "\\result\\" + file.getOriginalFilename(); // 已处理的文本txt路径
        model.addAttribute("musician", biology);
        List<Incident> incidents = new ArrayList<>();
        List<Incident> allIncidents=new ArrayList<>();
        List<String> results = uploadService.mainPy(pyPath, inPath, outPath);
        for (int i = 0; i < results.size(); i += 4) {
            if (results.get(i).compareTo(biology.getStartTime()) > 0 && results.get(i).compareTo(biology.getEndTime()) < 0) {
                incidents.add(new Incident(results.get(i), results.get(i + 1), results.get(i + 2), results.get(i + 3)));
            }
            allIncidents.add(new Incident(results.get(i), results.get(i + 1), results.get(i + 2), results.get(i + 3)));
        }

        model.addAttribute("events", incidents);
        model.addAttribute("allEvent",allIncidents);
        return "timeline";
    }
}
