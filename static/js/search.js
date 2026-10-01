/**
 * Search Module
 * Handles product search functionality with autocomplete
 */

class ProductSearch {
    constructor() {
        this.searchInput = document.getElementById('product-search');
        this.searchResults = document.getElementById('search-results');
        this.clearButton = document.getElementById('clear-search');
        this.productInfo = document.getElementById('product-info');
        this.selectedProduct = null;
        this.debounceTimer = null;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Search input with debounce
        this.searchInput.addEventListener('input', (e) => {
            const query = e.target.value.trim();
            
            // Show/hide clear button
            if (query) {
                this.clearButton.style.display = 'block';
            } else {
                this.clearButton.style.display = 'none';
                this.hideResults();
            }
            
            // Debounce search
            clearTimeout(this.debounceTimer);
            this.debounceTimer = setTimeout(() => {
                if (query.length >= 2) {
                    this.search(query);
                } else if (query.length === 0) {
                    this.hideResults();
                }
            }, 300);
        });
        
        // Clear button
        this.clearButton.addEventListener('click', () => {
            this.clearSearch();
        });
        
        // Handle Enter key
        this.searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const query = this.searchInput.value.trim();
                if (query.length >= 2) {
                    this.search(query);
                }
            }
        });
    }
    
    async search(query) {
        try {
            const response = await fetch(`/api/products/search?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (data.success) {
                this.displayResults(data.results);
            } else {
                this.showError(data.error || 'Search failed');
            }
        } catch (error) {
            console.error('Search error:', error);
            this.showError('Failed to search products');
        }
    }
    
    displayResults(results) {
        this.searchResults.innerHTML = '';
        
        if (results.length === 0) {
            this.searchResults.innerHTML = '<div class="no-results">No products found</div>';
            this.searchResults.style.display = 'block';
            return;
        }
        
        results.forEach(product => {
            const item = this.createResultItem(product);
            this.searchResults.appendChild(item);
        });
        
        this.searchResults.style.display = 'block';
    }
    
    createResultItem(product) {
        const item = document.createElement('div');
        item.className = 'search-result-item';
        
        item.innerHTML = `
            <div class="result-name">${product.name}</div>
            <div class="result-meta">${product.category} • ${product.aisle}</div>
        `;
        
        item.addEventListener('click', () => {
            this.selectProduct(product);
        });
        
        return item;
    }
    
    selectProduct(product) {
        this.selectedProduct = product;
        
        // Update search input
        this.searchInput.value = product.name;
        
        // Hide results
        this.hideResults();
        
        // Show product info
        this.showProductInfo(product);
        
        // Highlight on map
        if (window.mapInstance) {
            window.mapInstance.highlightProductLocation(product.node);
        }
        
        // Enable route button
        const routeBtn = document.getElementById('find-route-btn');
        if (routeBtn) {
            routeBtn.disabled = false;
        }
        
        // Dispatch event for other modules
        document.dispatchEvent(new CustomEvent('productSelected', { detail: product }));
    }
    
    showProductInfo(product) {
        document.getElementById('selected-product-name').textContent = product.name;
        document.getElementById('selected-product-category').textContent = product.category;
        document.getElementById('selected-product-aisle').textContent = product.aisle;
        document.getElementById('selected-product-shelf').textContent = product.shelf || 'N/A';
        
        this.productInfo.style.display = 'block';
        
        // Smooth animation
        this.productInfo.style.animation = 'slideIn 0.3s ease-out';
    }
    
    hideResults() {
        this.searchResults.style.display = 'none';
        this.searchResults.innerHTML = '';
    }
    
    clearSearch() {
        this.searchInput.value = '';
        this.clearButton.style.display = 'none';
        this.hideResults();
        this.clearSelection();
    }
    
    clearSelection() {
        this.selectedProduct = null;
        this.productInfo.style.display = 'none';
        
        // Clear map highlights
        if (window.mapInstance) {
            window.mapInstance.clearHighlights();
        }
        
        // Disable route button
        const routeBtn = document.getElementById('find-route-btn');
        if (routeBtn) {
            routeBtn.disabled = true;
        }
        
        // Dispatch event
        document.dispatchEvent(new CustomEvent('productDeselected'));
    }
    
    showError(message) {
        this.searchResults.innerHTML = `<div class="no-results" style="color: #C94D3A;">${message}</div>`;
        this.searchResults.style.display = 'block';
    }
    
    getSelectedProduct() {
        return this.selectedProduct;
    }
}

// Export for use in other modules
window.ProductSearch = ProductSearch;
