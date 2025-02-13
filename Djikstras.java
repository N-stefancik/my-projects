

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class Djikstras {

    public List<Node> dijkstraShortestPath(Graph graph, String startNodeId, String endNodeId) {
        Map<String, Double> distances = new HashMap<>();
        Map<String, String> previousNodes = new HashMap<>();
        PriorityQueue<NodeDistancePair> priorityQueue = new PriorityQueue<>(Comparator.comparingDouble(NodeDistancePair::getDistance));

        // Initialize distances to infinity
        for (String nodeId : graph.getMap().keySet()) {
            distances.put(nodeId, Double.MAX_VALUE);
        }
        distances.put(startNodeId, 0.0);
        priorityQueue.add(new NodeDistancePair(startNodeId, 0.0));

        while (!priorityQueue.isEmpty()) {
            NodeDistancePair currentPair = priorityQueue.poll();
            String currentNodeId = currentPair.getNodeId();
            Node currentNode = graph.getNode(currentNodeId);

            // Process each neighbor
            for (Edge edge : currentNode.getEdges()) {
                Node neighbor = edge.getEnding();
                double newDistance = distances.get(currentNodeId) + edge.getWeight();

                if (newDistance < distances.get(neighbor.getId())) {
                    distances.put(neighbor.getId(), newDistance);
                    previousNodes.put(neighbor.getId(), currentNodeId);
                    priorityQueue.add(new NodeDistancePair(neighbor.getId(), newDistance));
                }
            }
        }

        // Return the reconstructed path
        return reconstructPath(graph, previousNodes, startNodeId, endNodeId);
    }

    private List<Node> reconstructPath(Graph graph, Map<String, String> previousNodes, String startNodeId, String endNodeId) {
        List<Node> path = new ArrayList<>();
        Node currentNode = graph.getNode(endNodeId);

        while (currentNode != null) {
            path.add(currentNode);
            if (currentNode.getId().equals(startNodeId)) break;
            currentNode = graph.getNode(previousNodes.get(currentNode.getId()));
        }

        if (path.isEmpty() || !path.get(path.size() - 1).getId().equals(startNodeId)) {
            return Collections.emptyList(); // No path exists
        }

        Collections.reverse(path); // Reverse to start from the source
        return path;
    }

    // Helper class for priority queue
    private static class NodeDistancePair {
        private final String nodeId;
        private final double distance;

        public NodeDistancePair(String nodeId, double distance) {
            this.nodeId = nodeId;
            this.distance = distance;
        }

        public String getNodeId() {
            return nodeId;
        }

        public double getDistance() {
            return distance;
        }
    }
}
    
    
    
    
