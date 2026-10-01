/**
 * Navigation Module
 * Handles route calculation and navigation instructions
 */

class NavigationController {
    constructor(searchInstance, mapInstance) {
        this.search = searchInstance;
        this.map = mapInstance;
        this.currentRoute = null;
        
        this.findRouteBtn = document.getElementById('find-route-btn');
        this.resetRouteBtn = document.getElementById('reset-route-btn');
        this.startPointSelect = document.getElementById('start-point');
        this.routeInfo = document.getElementById('route-info');
        this.loadingState = document.getElementById('loading-state');
        this.errorMessage = document.getElementById('error-message');
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Find route button
        this.findRouteBtn.addEventListener('click', () => {
            this.calculateRoute();
        });
        
        // Reset route button
        this.resetRouteBtn.addEventListener('click', () => {
            this.resetNavigation();
        });
    }
    
    async calculateRoute() {
        const selectedProduct = this.search.getSelectedProduct();
        
        if (!selectedProduct) {
            this.showError('Please select a product first');
            return;
        }
        
        const startNode = this.startPointSelect.value;
        const destinationNode = selectedProduct.node;
        
        // Show loading state
        this.showLoading();
        this.hideError();
        
        try {
            const response = await fetch('/api/route', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    start: startNode,
                    destination: destinationNode
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.currentRoute = data;
                this.displayRoute(data);
                this.map.drawRoute(data.path_details);
            } else {
                this.showError(data.error || 'Failed to calculate route');
            }
        } catch (error) {
            console.error('Route calculation error:', error);
            this.showError('Failed to calculate route. Please try again.');
        } finally {
            this.hideLoading();
        }
    }
    
    displayRoute(routeData) {
        // Update route statistics
        document.getElementById('route-distance').textContent = routeData.distance;
        document.getElementById('route-time').textContent = routeData.estimated_time;
        document.getElementById('route-steps').textContent = routeData.steps;
        
        // Display navigation instructions
        this.displayInstructions(routeData.instructions || []);
        
        // Show route info panel
        this.routeInfo.style.display = 'block';
        
        // Hide find route button, show in route info instead
        this.findRouteBtn.style.display = 'none';
        
        // Scroll to route info
        this.routeInfo.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
    displayInstructions(instructions) {
        const instructionsList = document.getElementById('instructions-list');
        instructionsList.innerHTML = '';
        
        if (instructions.length === 0) {
            instructionsList.innerHTML = '<div class="no-results">No instructions available</div>';
            return;
        }
        
        instructions.forEach((instruction, index) => {
            const item = document.createElement('div');
            item.className = 'instruction-item';
            item.innerHTML = `<strong>${index + 1}.</strong> ${instruction}`;
            instructionsList.appendChild(item);
        });
    }
    
    resetNavigation() {
        // Clear route data
        this.currentRoute = null;
        
        // Hide route info
        this.routeInfo.style.display = 'none';
        
        // Show find route button
        this.findRouteBtn.style.display = 'block';
        
        // Clear map route
        this.map.clearRoute();
        
        // Clear product selection
        this.search.clearSearch();
        
        // Reset view
        this.map.resetView();
        
        // Hide error
        this.hideError();
    }
    
    showLoading() {
        this.loadingState.style.display = 'block';
        this.findRouteBtn.disabled = true;
    }
    
    hideLoading() {
        this.loadingState.style.display = 'none';
        this.findRouteBtn.disabled = false;
    }
    
    showError(message) {
        this.errorMessage.textContent = message;
        this.errorMessage.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            this.hideError();
        }, 5000);
    }
    
    hideError() {
        this.errorMessage.style.display = 'none';
    }
    
    getCurrentRoute() {
        return this.currentRoute;
    }
}

// Export for use in other modules
window.NavigationController = NavigationController;
