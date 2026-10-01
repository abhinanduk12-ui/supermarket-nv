"""
Dijkstra's Shortest Path Algorithm Implementation

This module implements Dijkstra's algorithm for finding the shortest path
in a weighted graph representing the supermarket floor plan.
"""

import heapq
from typing import Dict, List, Tuple, Optional


def dijkstra(graph: Dict[str, Dict[str, float]], start: str, destination: str) -> Tuple[Optional[List[str]], float, List[str]]:
    """
    Implements Dijkstra's shortest path algorithm.
    
    Args:
        graph: Dictionary representing the weighted graph
               Format: {node: {neighbor: weight, ...}, ...}
        start: Starting node identifier
        destination: Destination node identifier
    
    Returns:
        Tuple containing:
        - path: List of nodes from start to destination (None if no path exists)
        - distance: Total distance of the shortest path (float('inf') if no path)
        - visited: List of all visited nodes during the algorithm execution
    
    Raises:
        ValueError: If start or destination node doesn't exist in the graph
    """
    
    # Validate inputs
    if start not in graph:
        raise ValueError(f"Start node '{start}' not found in graph")
    if destination not in graph:
        raise ValueError(f"Destination node '{destination}' not found in graph")
    
    # Handle the case where start equals destination
    if start == destination:
        return [start], 0.0, [start]
    
    # Initialize data structures
    distances = {node: float('inf') for node in graph}
    distances[start] = 0.0
    
    # Priority queue: (distance, node)
    priority_queue = [(0.0, start)]
    
    # Track previous nodes for path reconstruction
    previous_nodes = {node: None for node in graph}
    
    # Track visited nodes
    visited = []
    visited_set = set()
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Skip if we've already processed this node
        if current_node in visited_set:
            continue
        
        # Mark as visited
        visited.append(current_node)
        visited_set.add(current_node)
        
        # If we reached the destination, we can stop
        if current_node == destination:
            break
        
        # Skip if this is an outdated entry
        if current_distance > distances[current_node]:
            continue
        
        # Check all neighbors
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            # If we found a shorter path, update it
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    # Reconstruct the shortest path
    if distances[destination] == float('inf'):
        # No path exists
        return None, float('inf'), visited
    
    # Build path from destination back to start
    path = []
    current = destination
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    
    # Reverse to get path from start to destination
    path.reverse()
    
    return path, distances[destination], visited


def calculate_route_steps(path: List[str], graph: Dict[str, Dict[str, float]]) -> List[Dict[str, any]]:
    """
    Calculate navigation steps from a path.
    
    Args:
        path: List of nodes in the route
        graph: The graph with edge weights
    
    Returns:
        List of navigation steps with distances
    """
    if not path or len(path) < 2:
        return []
    
    steps = []
    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]
        distance = graph[current].get(next_node, 0.0)
        
        steps.append({
            'from': current,
            'to': next_node,
            'distance': distance,
            'step_number': i + 1
        })
    
    return steps
