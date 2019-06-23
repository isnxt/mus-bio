package mocom.musician.entity;

public class Biology {
    private String musician;
    private String startTime;
    private String endTime;

    public void setMusician(String musician) {
        this.musician = musician;
    }

    public String getMusician() {
        return musician;
    }

    public String getStartTime() {
        return startTime;
    }

    public String getEndTime() {
        return endTime;
    }

    public void setEndTime(String endTime) {
        this.endTime = endTime;
    }

    public void setStartTime(String startTime) {
        this.startTime = startTime;
    }
}
