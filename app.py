"""
Supermarket 2D Navigator
Main Flask Application

A professional indoor supermarket navigation system that uses Dijkstra's
shortest-path algorithm to find optimal routes between products.
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
from backend.routes.products import products_bp
from backend.routes.navigation import navigation_bp

# Initialize Flask application
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Enable CORS for API access
CORS(app)

# Register blueprints
app.register_blueprint(products_bp)
app.register_blueprint(navigation_bp)


@app.route('/')
def index():
    """Render the main application page"""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'service': 'Supermarket 2D Navigator API',
        'version': '1.0.0'
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🏪 Supermarket 2D Navigator")
    print("=" * 60)
    print("🚀 Starting Flask server...")
    print("📍 Access the application at: http://localhost:5001")
    print("🔗 API Documentation: http://localhost:5001/api/health")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5001)
