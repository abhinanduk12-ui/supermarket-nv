"""
Navigation Routes
API endpoints for route calculation and navigation
"""

from flask import Blueprint, jsonify, request
from backend.services.navigation_service import NavigationService

navigation_bp = Blueprint('navigation', __name__)
navigation_service = NavigationService()


@navigation_bp.route('/api/route', methods=['POST'])
def calculate_route():
    """Calculate the shortest route between two points"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400
    
    start = data.get('start')
    destination = data.get('destination')
    
    if not start or not destination:
        return jsonify({
            'success': False,
            'error': 'Both start and destination are required'
        }), 400
    
    result = navigation_service.calculate_route(start, destination)
    
    # Generate navigation instructions if route was found
    if result['success'] and result.get('path_details') and result.get('detailed_steps'):
        instructions = navigation_service.generate_navigation_instructions(
            result['path_details'],
            result['detailed_steps']
        )
        result['instructions'] = instructions
    
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code


@navigation_bp.route('/api/graph/nodes', methods=['GET'])
def get_nodes():
    """Get all graph nodes"""
    nodes = navigation_service.get_all_nodes()
    
    return jsonify({
        'success': True,
        'count': len(nodes),
        'nodes': nodes
    })


@navigation_bp.route('/api/graph/nodes/<node_id>', methods=['GET'])
def get_node(node_id):
    """Get information about a specific node"""
    node = navigation_service.get_node_info(node_id)
    
    if node:
        return jsonify({
            'success': True,
            'node_id': node_id,
            'node': node
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Node not found'
        }), 404


@navigation_bp.route('/api/graph/edges', methods=['GET'])
def get_edges():
    """Get all graph edges"""
    edges = navigation_service.get_graph_edges()
    
    return jsonify({
        'success': True,
        'edges': edges
    })
