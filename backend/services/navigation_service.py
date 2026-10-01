"""
Navigation Service
Handles route calculation and navigation logic
"""

import json
from typing import Dict, List, Tuple, Optional
from backend.algorithms.dijkstra import dijkstra, calculate_route_steps


class NavigationService:
    """Service class for navigation and routing operations"""
    
    def __init__(self, graph_file: str = 'backend/data/graph.json'):
        """
        Initialize the navigation service
        
        Args:
            graph_file: Path to the graph JSON file
        """
        self.graph_file = graph_file
        self.graph_data = self._load_graph()
        self.nodes = self.graph_data.get('nodes', {})
        self.edges = self.graph_data.get('edges', {})
    
    def _load_graph(self) -> Dict:
        """Load graph data from JSON file"""
        try:
            with open(self.graph_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Graph file {self.graph_file} not found")
            return {'nodes': {}, 'edges': {}}
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in {self.graph_file}")
            return {'nodes': {}, 'edges': {}}
    
    def calculate_route(self, start: str, destination: str) -> Dict:
        """
        Calculate the shortest route between two nodes
        
        Args:
            start: Starting node identifier
            destination: Destination node identifier
        
        Returns:
            Dictionary containing route information
        """
        try:
            # Run Dijkstra's algorithm
            path, distance, visited = dijkstra(self.edges, start, destination)
            
            if path is None:
                return {
                    'success': False,
                    'error': 'No route found between the specified locations',
                    'path': None,
                    'distance': None,
                    'estimated_time': None,
                    'steps': 0
                }
            
            # Calculate estimated walking time (assuming 1.4 m/s walking speed)
            # distance is in meters, time in seconds
            estimated_time = int(distance / 1.4)
            
            # Get detailed steps
            steps = calculate_route_steps(path, self.edges)
            
            # Get node details for the path
            path_details = []
            for node_id in path:
                node_info = self.nodes.get(node_id, {})
                path_details.append({
                    'id': node_id,
                    'name': node_info.get('name', node_id),
                    'x': node_info.get('x', 0),
                    'y': node_info.get('y', 0),
                    'type': node_info.get('type', 'unknown')
                })
            
            return {
                'success': True,
                'path': path,
                'path_details': path_details,
                'distance': round(distance, 1),
                'estimated_time': estimated_time,
                'steps': len(path),
                'detailed_steps': steps,
                'visited_nodes': visited
            }
        
        except ValueError as e:
            return {
                'success': False,
                'error': str(e),
                'path': None,
                'distance': None,
                'estimated_time': None,
                'steps': 0
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'An error occurred during route calculation: {str(e)}',
                'path': None,
                'distance': None,
                'estimated_time': None,
                'steps': 0
            }
    
    def get_node_info(self, node_id: str) -> Optional[Dict]:
        """
        Get information about a specific node
        
        Args:
            node_id: Node identifier
        
        Returns:
            Node information dictionary or None
        """
        return self.nodes.get(node_id)
    
    def get_all_nodes(self) -> Dict:
        """
        Get all nodes in the graph
        
        Returns:
            Dictionary of all nodes
        """
        return self.nodes
    
    def get_graph_edges(self) -> Dict:
        """
        Get all edges in the graph
        
        Returns:
            Dictionary of all edges
        """
        return self.edges
    
    def generate_navigation_instructions(self, path_details: List[Dict], detailed_steps: List[Dict]) -> List[str]:
        """
        Generate human-readable navigation instructions
        
        Args:
            path_details: List of path nodes with details
            detailed_steps: List of detailed step information
        
        Returns:
            List of instruction strings
        """
        if not path_details or len(path_details) < 2:
            return []
        
        instructions = []
        
        # Starting instruction
        start_node = path_details[0]
        instructions.append(f"Start at {start_node['name']}")
        
        # Middle instructions
        for i, step in enumerate(detailed_steps):
            from_node = next((n for n in path_details if n['id'] == step['from']), None)
            to_node = next((n for n in path_details if n['id'] == step['to']), None)
            
            if from_node and to_node:
                distance = step['distance']
                
                # Determine direction based on node types and positions
                if 'aisle' in to_node['type']:
                    instructions.append(f"Walk {distance}m to {to_node['name']}")
                elif 'junction' in to_node['type']:
                    instructions.append(f"Continue {distance}m to {to_node['name']}")
                else:
                    instructions.append(f"Proceed {distance}m to {to_node['name']}")
        
        # Destination instruction
        destination = path_details[-1]
        instructions.append(f"You have arrived at {destination['name']}")
        
        return instructions
