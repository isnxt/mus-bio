package mocom.musician.service;

import mocom.musician.entity.Musician;
import mocom.musician.mapper.MusicianMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

@Service(value = "MusicianService")
public class MusicianService {
    @Autowired
    private MusicianMapper musicianMapper;

    private List<Musician> musicians = new ArrayList<>();

    public void setMusicians(String name) {
        musicians = musicianMapper.getInformation(name);
    }

    public List<String> getLocation() {
        List<String> location = new ArrayList<>();
        for (Musician str : musicians) {
            location.add(str.getLatitude() + "," + str.getLongitude());
        }
        return location;
    }

    public List<String> getDescription() {
        List<String> desc = new ArrayList<>();
        for (Musician str : musicians) {
            desc.add("<h3 style='color: #1e5ea7'>" + str.getDate() + "</h3> <h3 style='color: #1ea7a0'>" + str.getPeoples() + "</h3> <h3 style='color: #666b6b'>" + str.getCity() + "</h3> " + str.getDescription());
        }
        return desc;
    }

    public List<String> getMusician() {
        List<String> name = new ArrayList<>();
        List<String> nameList = musicianMapper.getAllMusician();
        Random random = new Random();
        for (int i = 0; i < 6; i++) {
            name.add(nameList.get(random.nextInt(nameList.size())));
        }
        return name;
    }

    public List<String> getAllMusician() {
        return musicianMapper.getAllMusician();
    }
}
