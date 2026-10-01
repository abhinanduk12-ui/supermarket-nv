"""
Unit Tests for Flask API Endpoints
"""

import unittest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


class TestProductAPI(unittest.TestCase):
    """Test cases for product API endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_get_all_products(self):
        """Test getting all products"""
        response = self.client.get('/api/products')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('products', data)
        self.assertGreater(data['count'], 0)
    
    def test_search_products(self):
        """Test product search"""
        response = self.client.get('/api/products/search?q=milk')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('results', data)
        self.assertGreater(len(data['results']), 0)
    
    def test_search_empty_query(self):
        """Test search with empty query"""
        response = self.client.get('/api/products/search?q=')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
    
    def test_search_no_results(self):
        """Test search with no matching products"""
        response = self.client.get('/api/products/search?q=nonexistentproduct12345')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['results']), 0)
    
    def test_get_product_by_id(self):
        """Test getting specific product"""
        response = self.client.get('/api/products/P001')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('product', data)
        self.assertEqual(data['product']['id'], 'P001')
    
    def test_get_nonexistent_product(self):
        """Test getting non-existent product"""
        response = self.client.get('/api/products/INVALID')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
    
    def test_get_categories(self):
        """Test getting all categories"""
        response = self.client.get('/api/categories')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('categories', data)
        self.assertGreater(len(data['categories']), 0)


class TestNavigationAPI(unittest.TestCase):
    """Test cases for navigation API endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_calculate_valid_route(self):
        """Test calculating a valid route"""
        payload = {
            'start': 'entrance',
            'destination': 'aisle_1_mid'
        }
        
        response = self.client.post(
            '/api/route',
            data=json.dumps(payload),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('path', data)
        self.assertIn('distance', data)
        self.assertIn('estimated_time', data)
        self.assertGreater(len(data['path']), 0)
    
    def test_calculate_route_missing_data(self):
        """Test route calculation with missing data"""
        payload = {
            'start': 'entrance'
            # Missing destination
        }
        
        response = self.client.post(
            '/api/route',
            data=json.dumps(payload),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
    
    def test_calculate_route_invalid_nodes(self):
        """Test route calculation with invalid nodes"""
        payload = {
            'start': 'invalid_start',
            'destination': 'invalid_destination'
        }
        
        response = self.client.post(
            '/api/route',
            data=json.dumps(payload),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
    
    def test_get_graph_nodes(self):
        """Test getting all graph nodes"""
        response = self.client.get('/api/graph/nodes')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('nodes', data)
        self.assertGreater(data['count'], 0)
    
    def test_get_specific_node(self):
        """Test getting specific node info"""
        response = self.client.get('/api/graph/nodes/entrance')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('node', data)
    
    def test_get_nonexistent_node(self):
        """Test getting non-existent node"""
        response = self.client.get('/api/graph/nodes/invalid_node')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
    
    def test_get_graph_edges(self):
        """Test getting all graph edges"""
        response = self.client.get('/api/graph/edges')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('edges', data)


class TestApplicationEndpoints(unittest.TestCase):
    """Test cases for general application endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_index_page(self):
        """Test main index page loads"""
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SuperNav', response.data)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['status'], 'healthy')
    
    def test_404_error(self):
        """Test 404 error handling"""
        response = self.client.get('/nonexistent-endpoint')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])


if __name__ == '__main__':
    unittest.main()
