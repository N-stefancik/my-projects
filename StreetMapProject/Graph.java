

import java.util.HashMap;
import java.util.Map;

public class Graph{

    private Map<String, Node> nodes;


    public Graph(){
        nodes = new HashMap<>();
    }

    public void addNode(String id, double latitude, double longitude){
        nodes.putIfAbsent(id, new Node(id, latitude, longitude));
    }

    public Node getNode(String id){
        return nodes.get(id);
    }

    public void addEdge(String node1ID, String node2ID, String id){

        Node node1 = nodes.get(node1ID);
        Node node2 = nodes.get(node2ID);

        if (node1 == null || node2 == null) {
            System.out.println(node1);
            System.out.println(node2);
            
            throw new IllegalArgumentException("Source or Destination node not found");
        }

        double weight = Math.sqrt((node1.getLatitude()-node2.getLatitude())*(node1.getLatitude()-node2.getLatitude()) + (node1.getLongitude()-node2.getLongitude())*(node1.getLongitude()-node2.getLongitude()));
        Edge edge1 = new Edge(weight, node1, node2, id);
        Edge edge2 = new Edge(weight, node2, node1, id);

        node1.addEdges(edge1);
        node2.addEdges(edge2);
    }

    public Map<String, Node> getMap(){
        return nodes;
    }

    public int size(){
        return nodes.size();
    }

}
