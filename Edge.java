

public class Edge{

    private Node begining;
    private Node ending;
    private double weight;
    private String id;

    public  Edge(double weight, Node begining, Node ending, String id){

        this.weight = weight;
        this.ending = ending;
        this.begining = begining;
        this.id = id;

    }

    public double getWeight(){
        return weight;
    }

    public Node getBegining(){
        return begining;
    }

    public Node getEnding(){
        return ending;
    }

    public String getId(){
        return id;
    }


}