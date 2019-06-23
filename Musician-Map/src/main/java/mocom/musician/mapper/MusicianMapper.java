package mocom.musician.mapper;

import mocom.musician.entity.Musician;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MusicianMapper {
    List<String> getAllMusician();

    List<Musician> getInformation(@Param("title") String musician);
}
