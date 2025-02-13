import java.awt.*;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import javax.swing.*;
import java.util.*;

public class StreetMap extends JPanel {
    private Graph roadMap;
    private    java.util.List<Node> shortestPathNodes;

    public StreetMap(Graph roadMap,    java.util.List<Node> shortestPathNodes) {
        this.roadMap = roadMap;
        this.shortestPathNodes = shortestPathNodes;
        setPreferredSize(new Dimension(800, 600));
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;

        // Set dimensions and scaling
        int panelWidth = getWidth();
        int panelHeight = getHeight();
        double minLat = 360, maxLat = -360, minLon = 360, maxLon = -360;

        // Find boundaries
        for (Node node : roadMap.getMap().values()) {
            double lat = node.getLatitude(), lon = node.getLongitude();
            minLat = Math.min(minLat, lat);
            maxLat = Math.max(maxLat, lat);
            minLon = Math.min(minLon, lon);
            maxLon = Math.max(maxLon, lon);
        }

        double latRange = Math.max(maxLat - minLat, 0.001);
        double lonRange = Math.max(maxLon - minLon, 0.001);
        double scale = Math.min(panelWidth / lonRange, panelHeight / latRange);

        // Draw all nodes and edges
        g2d.setStroke(new BasicStroke(1));
        g2d.setColor(new Color(211, 211, 211));
        for (Node node : roadMap.getMap().values()) {
            for (Edge edge : node.getEdges()) {
                Node node2 = edge.getEnding();
                int x1 = (int) ((node.getLongitude() - minLon) * scale);
                int y1 = (int) ((maxLat - node.getLatitude()) * scale);
                int x2 = (int) ((node2.getLongitude() - minLon) * scale);
                int y2 = (int) ((maxLat - node2.getLatitude()) * scale);
                g2d.drawLine(x1, y1, x2, y2);
            }
        }

        // Draw shortest path if available
        if (shortestPathNodes != null) {
            g2d.setStroke(new BasicStroke(3));
            g2d.setColor(new Color(45, 34, 122));
            for (int i = 0; i < shortestPathNodes.size() - 1; i++) {
                Node n1 = shortestPathNodes.get(i), n2 = shortestPathNodes.get(i + 1);
                int x1 = (int) ((n1.getLongitude() - minLon) * scale);
                int y1 = (int) ((maxLat - n1.getLatitude()) * scale);
                int x2 = (int) ((n2.getLongitude() - minLon) * scale);
                int y2 = (int) ((maxLat - n2.getLatitude()) * scale);
                g2d.drawLine(x1, y1, x2, y2);
            }
        }
    }

    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java StreetMap <filename> [--show] [--directions start end]");
            return;
        }

        // Parse arguments
        String filename = args[0];
        boolean showMap = false;
        String startIntersection = null, endIntersection = null;

        for (int i = 1; i < args.length; i++) {
            if (args[i].equals("--show")) {
                showMap = true;
            } else if (args[i].equals("--directions") && i + 2 < args.length) {
                startIntersection = args[i + 1];
                endIntersection = args[i + 2];
                i += 2;
            }
        }

        // Load the map
        Graph roadMap = new Graph();
        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] parts = line.split("\t");
                if (parts[0].equals("i")) {
                    roadMap.addNode(parts[1], Double.parseDouble(parts[2]), Double.parseDouble(parts[3]));
                } else if (parts[0].equals("r")) {
                    roadMap.addEdge(parts[2], parts[3], parts[1]);
                }
            }
        } catch (IOException e) {
            System.err.println("Error loading map: " + e.getMessage());
            return;
        }

        // Compute directions if needed
        java.util.List<Node> shortestPath = null;
        if (startIntersection != null && endIntersection != null) {
            Djikstras dijkstra = new Djikstras();
            shortestPath = dijkstra.dijkstraShortestPath(roadMap, startIntersection, endIntersection);
            System.out.println("Shortest path:");
            for (Node node : shortestPath) {
                System.out.println(node.getId());
            }
        }

        // Show map if requested
        if (showMap) {
            JFrame frame = new JFrame("Street Map");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.add(new MapDrawing(roadMap, shortestPath));
            frame.pack();
            frame.setVisible(true);
        }
    }
}