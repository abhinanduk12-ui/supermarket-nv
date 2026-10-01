#!/usr/bin/env python3
"""
Verification Script for Supermarket 2D Navigator
Tests that all components are working correctly
"""

import json
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} missing: {filepath}")
        return False

def check_json_valid(filepath, description):
    """Check if JSON file is valid"""
    try:
        with open(filepath, 'r') as f:
            json.load(f)
        print(f"✅ {description} valid: {filepath}")
        return True
    except Exception as e:
        print(f"❌ {description} invalid: {filepath} - {e}")
        return False

def main():
    print("=" * 60)
    print("🔍 Supermarket 2D Navigator - Verification")
    print("=" * 60)
    print()
    
    checks_passed = 0
    checks_total = 0
    
    # Check core files
    print("📁 Checking Core Files...")
    files_to_check = [
        ('app.py', 'Main application'),
        ('requirements.txt', 'Dependencies'),
        ('README.md', 'Documentation'),
        ('templates/index.html', 'HTML template'),
        ('static/css/style.css', 'Stylesheet'),
    ]
    
    for filepath, desc in files_to_check:
        checks_total += 1
        if check_file_exists(filepath, desc):
            checks_passed += 1
    
    print()
    
    # Check JavaScript files
    print("📜 Checking JavaScript Files...")
    js_files = [
        ('static/js/app.js', 'Main app'),
        ('static/js/map.js', 'Map module'),
        ('static/js/search.js', 'Search module'),
        ('static/js/navigation.js', 'Navigation module'),
    ]
    
    for filepath, desc in js_files:
        checks_total += 1
        if check_file_exists(filepath, desc):
            checks_passed += 1
    
    print()
    
    # Check backend modules
    print("🐍 Checking Backend Modules...")
    backend_files = [
        ('backend/algorithms/dijkstra.py', 'Dijkstra algorithm'),
        ('backend/services/product_service.py', 'Product service'),
        ('backend/services/navigation_service.py', 'Navigation service'),
        ('backend/routes/products.py', 'Product routes'),
        ('backend/routes/navigation.py', 'Navigation routes'),
    ]
    
    for filepath, desc in backend_files:
        checks_total += 1
        if check_file_exists(filepath, desc):
            checks_passed += 1
    
    print()
    
    # Check data files
    print("📊 Checking Data Files...")
    checks_total += 1
    if check_json_valid('backend/data/products.json', 'Products data'):
        checks_passed += 1
        
        # Count products
        with open('backend/data/products.json', 'r') as f:
            products = json.load(f)
            print(f"   → {len(products)} products loaded")
    
    checks_total += 1
    if check_json_valid('backend/data/graph.json', 'Graph data'):
        checks_passed += 1
        
        # Count nodes
        with open('backend/data/graph.json', 'r') as f:
            graph = json.load(f)
            print(f"   → {len(graph['nodes'])} nodes, {len(graph['edges'])} edge groups")
    
    print()
    
    # Check test files
    print("🧪 Checking Test Files...")
    test_files = [
        ('tests/test_dijkstra.py', 'Algorithm tests'),
        ('tests/test_api.py', 'API tests'),
    ]
    
    for filepath, desc in test_files:
        checks_total += 1
        if check_file_exists(filepath, desc):
            checks_passed += 1
    
    print()
    
    # Test Dijkstra algorithm
    print("⚡ Testing Dijkstra Algorithm...")
    try:
        from backend.algorithms.dijkstra import dijkstra
        
        test_graph = {
            'A': {'B': 5.0},
            'B': {'A': 5.0, 'C': 3.0},
            'C': {'B': 3.0}
        }
        
        path, distance, visited = dijkstra(test_graph, 'A', 'C')
        
        if path == ['A', 'B', 'C'] and distance == 8.0:
            print(f"✅ Algorithm test passed: A → B → C = {distance}m")
            checks_passed += 1
        else:
            print(f"❌ Algorithm test failed: unexpected result")
        checks_total += 1
    except Exception as e:
        print(f"❌ Algorithm test error: {e}")
        checks_total += 1
    
    print()
    
    # Summary
    print("=" * 60)
    print(f"📊 Verification Results: {checks_passed}/{checks_total} checks passed")
    print("=" * 60)
    
    if checks_passed == checks_total:
        print("✅ All checks passed! Application is ready to run.")
        print()
        print("To start the application:")
        print("  python3 app.py")
        print()
        print("Then open: http://localhost:5001")
        return 0
    else:
        print(f"⚠️  {checks_total - checks_passed} checks failed.")
        print("Please review the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
