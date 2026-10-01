"""
Product Routes
API endpoints for product operations
"""

from flask import Blueprint, jsonify, request
from backend.services.product_service import ProductService

products_bp = Blueprint('products', __name__)
product_service = ProductService()


@products_bp.route('/api/products', methods=['GET'])
def get_all_products():
    """Get all products"""
    products = product_service.get_all_products()
    return jsonify({
        'success': True,
        'count': len(products),
        'products': products
    })


@products_bp.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    product = product_service.get_product_by_id(product_id)
    
    if product:
        return jsonify({
            'success': True,
            'product': product
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Product not found'
        }), 404


@products_bp.route('/api/products/search', methods=['GET'])
def search_products():
    """Search for products"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Search query is required'
        }), 400
    
    results = product_service.search_products(query)
    
    return jsonify({
        'success': True,
        'query': query,
        'count': len(results),
        'results': results
    })


@products_bp.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    categories = product_service.get_all_categories()
    
    return jsonify({
        'success': True,
        'categories': categories
    })


@products_bp.route('/api/products/category/<category>', methods=['GET'])
def get_products_by_category(category):
    """Get products by category"""
    products = product_service.get_products_by_category(category)
    
    return jsonify({
        'success': True,
        'category': category,
        'count': len(products),
        'products': products
    })
