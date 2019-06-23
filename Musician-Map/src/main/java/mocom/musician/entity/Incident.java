package mocom.musician.entity;

public class Incident {
    String people;
    String time;
    String place;
    String event;

    public Incident(String time, String people, String place, String event) {
        this.event = event;
        this.people = people;
        this.place = place;
        this.time = time;
    }

    public String getEvent() {
        this.event = event.replace("|", "");
        return event;
    }

    public String getPeople() {
        this.people = people.replace("|", "\t");
        return people;
    }

    public String getPlace() {
        this.place = place.replace("|", "\t");
        return place;
    }

    public String getTime() {
        this.time = time.replace("|", "");
        return time;
    }
}
