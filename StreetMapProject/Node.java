

import java.util.ArrayList;
import java.util.List;

public class Node{


    private String id;
    private double latitude;
    private double longitude;
    private List<Edge> edges;


    public Node(String id, double latitude, double longitude){
        this.id = id;
        this.latitude = latitude;
        this.longitude = longitude;
        this.edges = new ArrayList<>();
    }


    public String getId(){  
        return id;
    }


    public void addEdges(Edge edge){
        // make sure to do this both ways when building the edge
        edges.add(edge);
    }

    public List<Edge> getEdges(){
        return edges;
    }

    public double getLatitude(){
        return latitude;
    }

    public double getLongitude(){
        return longitude;
    }

}
