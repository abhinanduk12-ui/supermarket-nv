"""
Unit Tests for Dijkstra's Algorithm
"""

import unittest
from backend.algorithms.dijkstra import dijkstra, calculate_route_steps


class TestDijkstraAlgorithm(unittest.TestCase):
    """Test cases for Dijkstra's shortest path algorithm"""
    
    def setUp(self):
        """Set up test graph"""
        self.simple_graph = {
            'A': {'B': 5.0, 'C': 3.0},
            'B': {'A': 5.0, 'C': 2.0, 'D': 4.0},
            'C': {'A': 3.0, 'B': 2.0, 'D': 6.0},
            'D': {'B': 4.0, 'C': 6.0}
        }
        
        self.complex_graph = {
            'entrance': {'node_1': 10.0, 'node_2': 15.0},
            'node_1': {'entrance': 10.0, 'node_2': 5.0, 'destination': 20.0},
            'node_2': {'entrance': 15.0, 'node_1': 5.0, 'node_3': 8.0},
            'node_3': {'node_2': 8.0, 'destination': 10.0},
            'destination': {'node_1': 20.0, 'node_3': 10.0}
        }
    
    def test_basic_shortest_path(self):
        """Test basic shortest path calculation"""
        path, distance, visited = dijkstra(self.simple_graph, 'A', 'D')
        
        self.assertIsNotNone(path)
        self.assertEqual(path[0], 'A')
        self.assertEqual(path[-1], 'D')
        self.assertLess(distance, float('inf'))
        self.assertGreater(len(visited), 0)
    
    def test_optimal_path_selection(self):
        """Test that algorithm selects the optimal path"""
        path, distance, visited = dijkstra(self.simple_graph, 'A', 'D')
        
        # The optimal path should be A -> C -> D with distance 9
        # (A->C: 3, C->D: 6, total: 9)
        self.assertEqual(distance, 9.0)
        self.assertEqual(path, ['A', 'C', 'D'])
    
    def test_direct_path(self):
        """Test path when direct connection exists"""
        path, distance, visited = dijkstra(self.simple_graph, 'A', 'B')
        
        self.assertEqual(path, ['A', 'B'])
        self.assertEqual(distance, 5.0)
    
    def test_same_start_and_destination(self):
        """Test when start equals destination"""
        path, distance, visited = dijkstra(self.simple_graph, 'A', 'A')
        
        self.assertEqual(path, ['A'])
        self.assertEqual(distance, 0.0)
        self.assertEqual(visited, ['A'])
    
    def test_invalid_start_node(self):
        """Test error handling for invalid start node"""
        with self.assertRaises(ValueError) as context:
            dijkstra(self.simple_graph, 'INVALID', 'D')
        
        self.assertIn('Start node', str(context.exception))
    
    def test_invalid_destination_node(self):
        """Test error handling for invalid destination node"""
        with self.assertRaises(ValueError) as context:
            dijkstra(self.simple_graph, 'A', 'INVALID')
        
        self.assertIn('Destination node', str(context.exception))
    
    def test_unreachable_destination(self):
        """Test when destination is unreachable"""
        disconnected_graph = {
            'A': {'B': 5.0},
            'B': {'A': 5.0},
            'C': {'D': 3.0},
            'D': {'C': 3.0}
        }
        
        path, distance, visited = dijkstra(disconnected_graph, 'A', 'D')
        
        self.assertIsNone(path)
        self.assertEqual(distance, float('inf'))
    
    def test_complex_graph_routing(self):
        """Test routing in a more complex graph"""
        path, distance, visited = dijkstra(self.complex_graph, 'entrance', 'destination')
        
        self.assertIsNotNone(path)
        self.assertEqual(path[0], 'entrance')
        self.assertEqual(path[-1], 'destination')
        
        # The optimal path should be entrance -> node_1 -> destination
        # (entrance->node_1: 10, node_1->destination: 20, total: 30)
        self.assertEqual(distance, 30.0)
    
    def test_visited_nodes_tracking(self):
        """Test that visited nodes are properly tracked"""
        path, distance, visited = dijkstra(self.simple_graph, 'A', 'D')
        
        self.assertGreater(len(visited), 0)
        self.assertIn('A', visited)
        self.assertIn('D', visited)
        
        # Start node should be first visited
        self.assertEqual(visited[0], 'A')
    
    def test_calculate_route_steps(self):
        """Test route steps calculation"""
        path = ['A', 'C', 'B', 'D']
        steps = calculate_route_steps(path, self.simple_graph)
        
        self.assertEqual(len(steps), 3)  # 4 nodes = 3 steps
        
        # Check first step
        self.assertEqual(steps[0]['from'], 'A')
        self.assertEqual(steps[0]['to'], 'C')
        self.assertEqual(steps[0]['distance'], 3.0)
        self.assertEqual(steps[0]['step_number'], 1)
    
    def test_empty_path_steps(self):
        """Test steps calculation with empty path"""
        steps = calculate_route_steps([], self.simple_graph)
        self.assertEqual(steps, [])
    
    def test_single_node_path_steps(self):
        """Test steps calculation with single node"""
        steps = calculate_route_steps(['A'], self.simple_graph)
        self.assertEqual(steps, [])


class TestDijkstraPerformance(unittest.TestCase):
    """Performance tests for Dijkstra's algorithm"""
    
    def test_large_graph_performance(self):
        """Test algorithm performance on larger graph"""
        # Create a larger graph
        large_graph = {}
        num_nodes = 100
        
        for i in range(num_nodes):
            node = f'node_{i}'
            large_graph[node] = {}
            
            # Connect to next few nodes
            for j in range(i + 1, min(i + 5, num_nodes)):
                neighbor = f'node_{j}'
                distance = float((j - i) * 2)
                large_graph[node][neighbor] = distance
        
        import time
        start_time = time.time()
        
        path, distance, visited = dijkstra(large_graph, 'node_0', f'node_{num_nodes-1}')
        
        elapsed_time = time.time() - start_time
        
        # Should complete in reasonable time (< 1 second)
        self.assertLess(elapsed_time, 1.0)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], 'node_0')
        self.assertEqual(path[-1], f'node_{num_nodes-1}')


if __name__ == '__main__':
    unittest.main()
