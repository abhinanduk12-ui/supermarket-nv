"""
Product Service
Handles product-related business logic
"""

import json
from typing import List, Dict, Optional


class ProductService:
    """Service class for managing product operations"""
    
    def __init__(self, products_file: str = 'backend/data/products.json'):
        """
        Initialize the product service
        
        Args:
            products_file: Path to the products JSON file
        """
        self.products_file = products_file
        self.products = self._load_products()
    
    def _load_products(self) -> List[Dict]:
        """Load products from JSON file"""
        try:
            with open(self.products_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Products file {self.products_file} not found")
            return []
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in {self.products_file}")
            return []
    
    def get_all_products(self) -> List[Dict]:
        """
        Get all products
        
        Returns:
            List of all products
        """
        return self.products
    
    def get_product_by_id(self, product_id: str) -> Optional[Dict]:
        """
        Get a specific product by ID
        
        Args:
            product_id: Product identifier
        
        Returns:
            Product dictionary or None if not found
        """
        for product in self.products:
            if product['id'] == product_id:
                return product
        return None
    
    def search_products(self, query: str) -> List[Dict]:
        """
        Search for products by name or category
        
        Args:
            query: Search query string
        
        Returns:
            List of matching products
        """
        if not query:
            return []
        
        query_lower = query.lower().strip()
        results = []
        
        for product in self.products:
            # Search in name, category, and aisle
            if (query_lower in product['name'].lower() or
                query_lower in product['category'].lower() or
                query_lower in product['aisle'].lower()):
                results.append(product)
        
        return results
    
    def get_products_by_category(self, category: str) -> List[Dict]:
        """
        Get all products in a specific category
        
        Args:
            category: Category name
        
        Returns:
            List of products in the category
        """
        return [p for p in self.products if p['category'].lower() == category.lower()]
    
    def get_products_by_aisle(self, aisle: str) -> List[Dict]:
        """
        Get all products in a specific aisle
        
        Args:
            aisle: Aisle name
        
        Returns:
            List of products in the aisle
        """
        return [p for p in self.products if p['aisle'].lower() == aisle.lower()]
    
    def get_all_categories(self) -> List[str]:
        """
        Get list of all unique categories
        
        Returns:
            List of category names
        """
        categories = set(p['category'] for p in self.products)
        return sorted(list(categories))
