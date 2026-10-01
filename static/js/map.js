/**
 * Map Module
 * Handles SVG map creation, rendering, and interactions
 */

class SupermarketMap {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.svg = null;
        this.viewBox = { x: 0, y: 0, width: 1200, height: 600 };
        this.scale = 1;
        this.isPanning = false;
        this.startPoint = { x: 0, y: 0 };
        this.nodes = {};
        this.edges = {};
        this.selectedProductNode = null;
        this.currentRoute = null;
        
        this.init();
    }
    
    init() {
        this.createSVG();
        this.drawSupermarket();
        this.setupInteractions();
        this.loadGraphData();
    }
    
    createSVG() {
        this.svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        this.svg.setAttribute('class', 'supermarket-map');
        this.svg.setAttribute('viewBox', 
            `${this.viewBox.x} ${this.viewBox.y} ${this.viewBox.width} ${this.viewBox.height}`);
        this.container.appendChild(this.svg);
        
        // Create main group for all elements
        this.mainGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        this.svg.appendChild(this.mainGroup);
        
        // Create layers
        this.corridorLayer = this.createLayer('corridor-layer');
        this.aisleLayer = this.createLayer('aisle-layer');
        this.nodeLayer = this.createLayer('node-layer');
        this.routeLayer = this.createLayer('route-layer');
        this.markerLayer = this.createLayer('marker-layer');
    }
    
    createLayer(id) {
        const layer = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        layer.setAttribute('id', id);
        this.mainGroup.appendChild(layer);
        return layer;
    }
    
    drawSupermarket() {
        // Draw supermarket floor plan
        this.drawBoundary();
        this.drawAisles();
        this.drawSpecialAreas();
        this.drawLabels();
    }
    
    drawBoundary() {
        const boundary = this.createRect(50, 150, 1100, 400, {
            fill: '#FCFCF8',
            stroke: '#667A3E',
            strokeWidth: 3
        });
        this.corridorLayer.appendChild(boundary);
    }
    
    drawAisles() {
        const aisles = [
            { x: 280, y: 200, width: 40, height: 300, label: 'Aisle 1', number: 1 },
            { x: 480, y: 200, width: 40, height: 300, label: 'Aisle 2', number: 2 },
            { x: 680, y: 200, width: 40, height: 300, label: 'Aisle 3', number: 3 },
            { x: 880, y: 200, width: 40, height: 300, label: 'Aisle 4', number: 4 }
        ];
        
        aisles.forEach(aisle => {
            // Draw aisle shelves
            const rect = this.createRect(aisle.x, aisle.y, aisle.width, aisle.height, {
                fill: '#DCE5C5',
                stroke: '#667A3E',
                strokeWidth: 2,
                class: 'aisle-rect'
            });
            
            // Add hover tooltip
            const title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
            title.textContent = aisle.label;
            rect.appendChild(title);
            
            this.aisleLayer.appendChild(rect);
            
            // Draw aisle label
            const text = this.createText(
                aisle.x + aisle.width / 2,
                aisle.y - 10,
                aisle.label,
                {
                    fontSize: '14px',
                    fontWeight: '600',
                    fill: '#3F4D27',
                    textAnchor: 'middle'
                }
            );
            this.aisleLayer.appendChild(text);
        });
    }
    
    drawSpecialAreas() {
        // Entrance
        const entrance = this.createRect(70, 480, 60, 40, {
            fill: '#667A3E',
            stroke: '#3F4D27',
            strokeWidth: 2,
            rx: 8
        });
        this.aisleLayer.appendChild(entrance);
        
        const entranceText = this.createText(100, 505, 'ENTRANCE', {
            fontSize: '12px',
            fontWeight: 'bold',
            fill: '#FFFFFF',
            textAnchor: 'middle'
        });
        this.aisleLayer.appendChild(entranceText);
        
        // Checkout Area
        const checkout = this.createRect(1020, 480, 100, 40, {
            fill: '#3F4D27',
            stroke: '#29331B',
            strokeWidth: 2,
            rx: 8
        });
        this.aisleLayer.appendChild(checkout);
        
        const checkoutText = this.createText(1070, 505, 'CHECKOUT', {
            fontSize: '12px',
            fontWeight: 'bold',
            fill: '#FFFFFF',
            textAnchor: 'middle'
        });
        this.aisleLayer.appendChild(checkoutText);
        
        // Customer Service
        const service = this.createRect(1020, 330, 100, 40, {
            fill: '#8FA35A',
            stroke: '#667A3E',
            strokeWidth: 2,
            rx: 8
        });
        this.aisleLayer.appendChild(service);
        
        const serviceText = this.createText(1070, 350, 'SERVICE', {
            fontSize: '11px',
            fontWeight: '600',
            fill: '#29331B',
            textAnchor: 'middle'
        });
        this.aisleLayer.appendChild(serviceText);
    }
    
    drawLabels() {
        // Add section labels
        const sections = [
            { x: 300, y: 180, text: 'Dairy & Grains' },
            { x: 500, y: 180, text: 'Fresh Produce' },
            { x: 700, y: 180, text: 'Bakery & Household' },
            { x: 900, y: 180, text: 'Beverages & More' }
        ];
        
        sections.forEach(section => {
            const text = this.createText(section.x, section.y, section.text, {
                fontSize: '11px',
                fill: '#73786D',
                textAnchor: 'middle',
                fontStyle: 'italic'
            });
            this.aisleLayer.appendChild(text);
        });
    }
    
    async loadGraphData() {
        try {
            const response = await fetch('/api/graph/nodes');
            const data = await response.json();
            
            if (data.success) {
                this.nodes = data.nodes;
                this.drawNodes();
            }
        } catch (error) {
            console.error('Error loading graph data:', error);
        }
    }
    
    drawNodes() {
        Object.entries(this.nodes).forEach(([nodeId, node]) => {
            const circle = this.createCircle(node.x, node.y, 5, {
                fill: this.getNodeColor(node.type),
                stroke: '#667A3E',
                strokeWidth: 1.5,
                class: `node-circle node-${node.type}`,
                id: `node-${nodeId}`
            });
            
            const title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
            title.textContent = node.name;
            circle.appendChild(title);
            
            this.nodeLayer.appendChild(circle);
        });
    }
    
    getNodeColor(type) {
        const colors = {
            entrance: '#667A3E',
            checkout: '#3F4D27',
            service: '#8FA35A',
            junction: '#FFFFFF',
            aisle: '#F7F5EC',
            corridor: '#FFFFFF'
        };
        return colors[type] || '#FFFFFF';
    }
    
    highlightProductLocation(nodeId) {
        // Remove previous highlights
        this.clearHighlights();
        
        if (!nodeId || !this.nodes[nodeId]) return;
        
        const node = this.nodes[nodeId];
        this.selectedProductNode = nodeId;
        
        // Create pulsing marker
        const marker = this.createCircle(node.x, node.y, 12, {
            fill: '#C94D3A',
            class: 'product-marker',
            id: 'product-marker'
        });
        
        this.markerLayer.appendChild(marker);
        
        // Pan to the product location
        this.panToNode(nodeId);
    }
    
    drawRoute(pathDetails) {
        // Clear previous route
        this.clearRoute();
        
        if (!pathDetails || pathDetails.length < 2) return;
        
        this.currentRoute = pathDetails;
        
        // Create path string
        let pathString = `M ${pathDetails[0].x} ${pathDetails[0].y}`;
        for (let i = 1; i < pathDetails.length; i++) {
            pathString += ` L ${pathDetails[i].x} ${pathDetails[i].y}`;
        }
        
        // Draw the route path
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', pathString);
        path.setAttribute('class', 'route-path');
        path.setAttribute('id', 'route-path');
        
        this.routeLayer.appendChild(path);
        
        // Add start marker
        const startMarker = this.createCircle(pathDetails[0].x, pathDetails[0].y, 8, {
            fill: '#667A3E',
            stroke: '#FFFFFF',
            strokeWidth: 2,
            id: 'start-marker'
        });
        this.markerLayer.appendChild(startMarker);
        
        // Add end marker
        const endMarker = this.createCircle(
            pathDetails[pathDetails.length - 1].x,
            pathDetails[pathDetails.length - 1].y,
            10,
            {
                fill: '#C94D3A',
                stroke: '#FFFFFF',
                strokeWidth: 2,
                class: 'product-marker',
                id: 'end-marker'
            }
        );
        this.markerLayer.appendChild(endMarker);
        
        // Animate a moving marker along the route
        this.animateRouteMarker(pathDetails);
    }
    
    animateRouteMarker(pathDetails) {
        const marker = this.createCircle(pathDetails[0].x, pathDetails[0].y, 6, {
            fill: '#667A3E',
            class: 'route-marker',
            id: 'animated-marker'
        });
        this.markerLayer.appendChild(marker);
        
        // Calculate total path length for smooth animation
        let currentIndex = 0;
        const animationDuration = 3000; // 3 seconds
        const steps = 60;
        const interval = animationDuration / steps;
        
        const animate = () => {
            const progress = (currentIndex % steps) / steps;
            const totalSegments = pathDetails.length - 1;
            const segment = Math.floor(progress * totalSegments);
            const segmentProgress = (progress * totalSegments) - segment;
            
            if (segment < totalSegments) {
                const start = pathDetails[segment];
                const end = pathDetails[segment + 1];
                
                const x = start.x + (end.x - start.x) * segmentProgress;
                const y = start.y + (end.y - start.y) * segmentProgress;
                
                marker.setAttribute('cx', x);
                marker.setAttribute('cy', y);
            }
            
            currentIndex++;
            if (currentIndex < steps * 100) { // Loop animation
                requestAnimationFrame(animate);
            }
        };
        
        animate();
    }
    
    clearRoute() {
        const routePath = document.getElementById('route-path');
        const startMarker = document.getElementById('start-marker');
        const endMarker = document.getElementById('end-marker');
        const animatedMarker = document.getElementById('animated-marker');
        
        if (routePath) routePath.remove();
        if (startMarker) startMarker.remove();
        if (endMarker) endMarker.remove();
        if (animatedMarker) animatedMarker.remove();
        
        this.currentRoute = null;
    }
    
    clearHighlights() {
        const productMarker = document.getElementById('product-marker');
        if (productMarker) productMarker.remove();
        this.selectedProductNode = null;
    }
    
    panToNode(nodeId) {
        if (!this.nodes[nodeId]) return;
        
        const node = this.nodes[nodeId];
        const centerX = node.x - this.viewBox.width / 2;
        const centerY = node.y - this.viewBox.height / 2;
        
        // Smooth transition
        this.animateViewBox(centerX, centerY, this.viewBox.width, this.viewBox.height);
    }
    
    animateViewBox(targetX, targetY, targetWidth, targetHeight) {
        const startX = this.viewBox.x;
        const startY = this.viewBox.y;
        const duration = 500;
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function
            const easeProgress = progress < 0.5 
                ? 2 * progress * progress 
                : 1 - Math.pow(-2 * progress + 2, 2) / 2;
            
            this.viewBox.x = startX + (targetX - startX) * easeProgress;
            this.viewBox.y = startY + (targetY - startY) * easeProgress;
            
            this.updateViewBox();
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    }
    
    setupInteractions() {
        // Zoom controls
        document.getElementById('zoom-in')?.addEventListener('click', () => this.zoom(1.2));
        document.getElementById('zoom-out')?.addEventListener('click', () => this.zoom(0.8));
        document.getElementById('reset-view')?.addEventListener('click', () => this.resetView());
        
        // Pan with mouse
        this.svg.addEventListener('mousedown', (e) => this.handlePanStart(e));
        this.svg.addEventListener('mousemove', (e) => this.handlePanMove(e));
        this.svg.addEventListener('mouseup', () => this.handlePanEnd());
        this.svg.addEventListener('mouseleave', () => this.handlePanEnd());
        
        // Touch support
        this.svg.addEventListener('touchstart', (e) => this.handlePanStart(e));
        this.svg.addEventListener('touchmove', (e) => this.handlePanMove(e));
        this.svg.addEventListener('touchend', () => this.handlePanEnd());
    }
    
    zoom(factor) {
        const newWidth = this.viewBox.width / factor;
        const newHeight = this.viewBox.height / factor;
        
        // Keep center point
        const centerX = this.viewBox.x + this.viewBox.width / 2;
        const centerY = this.viewBox.y + this.viewBox.height / 2;
        
        this.viewBox.x = centerX - newWidth / 2;
        this.viewBox.y = centerY - newHeight / 2;
        this.viewBox.width = newWidth;
        this.viewBox.height = newHeight;
        
        // Limit zoom
        if (this.viewBox.width < 400) {
            this.viewBox.width = 400;
            this.viewBox.height = 200;
        }
        if (this.viewBox.width > 2000) {
            this.viewBox.width = 2000;
            this.viewBox.height = 1000;
        }
        
        this.updateViewBox();
    }
    
    handlePanStart(e) {
        this.isPanning = true;
        const point = this.getEventPoint(e);
        this.startPoint = { x: point.x - this.viewBox.x, y: point.y - this.viewBox.y };
        this.svg.style.cursor = 'grabbing';
    }
    
    handlePanMove(e) {
        if (!this.isPanning) return;
        
        e.preventDefault();
        const point = this.getEventPoint(e);
        
        this.viewBox.x = point.x - this.startPoint.x;
        this.viewBox.y = point.y - this.startPoint.y;
        
        this.updateViewBox();
    }
    
    handlePanEnd() {
        this.isPanning = false;
        this.svg.style.cursor = 'move';
    }
    
    getEventPoint(e) {
        const pt = this.svg.createSVGPoint();
        
        if (e.touches && e.touches.length > 0) {
            pt.x = e.touches[0].clientX;
            pt.y = e.touches[0].clientY;
        } else {
            pt.x = e.clientX;
            pt.y = e.clientY;
        }
        
        return pt.matrixTransform(this.svg.getScreenCTM().inverse());
    }
    
    resetView() {
        this.viewBox = { x: 0, y: 0, width: 1200, height: 600 };
        this.updateViewBox();
    }
    
    updateViewBox() {
        this.svg.setAttribute('viewBox', 
            `${this.viewBox.x} ${this.viewBox.y} ${this.viewBox.width} ${this.viewBox.height}`);
    }
    
    // Helper methods
    createRect(x, y, width, height, attrs = {}) {
        const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        rect.setAttribute('x', x);
        rect.setAttribute('y', y);
        rect.setAttribute('width', width);
        rect.setAttribute('height', height);
        
        Object.entries(attrs).forEach(([key, value]) => {
            if (key === 'class') {
                rect.setAttribute('class', value);
            } else if (key === 'strokeWidth') {
                rect.setAttribute('stroke-width', value);
            } else {
                rect.setAttribute(key, value);
            }
        });
        
        return rect;
    }
    
    createCircle(cx, cy, r, attrs = {}) {
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('cx', cx);
        circle.setAttribute('cy', cy);
        circle.setAttribute('r', r);
        
        Object.entries(attrs).forEach(([key, value]) => {
            if (key === 'class') {
                circle.setAttribute('class', value);
            } else if (key === 'strokeWidth') {
                circle.setAttribute('stroke-width', value);
            } else {
                circle.setAttribute(key, value);
            }
        });
        
        return circle;
    }
    
    createText(x, y, content, attrs = {}) {
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', x);
        text.setAttribute('y', y);
        text.textContent = content;
        
        Object.entries(attrs).forEach(([key, value]) => {
            if (key === 'fontSize') {
                text.setAttribute('font-size', value);
            } else if (key === 'fontWeight') {
                text.setAttribute('font-weight', value);
            } else if (key === 'textAnchor') {
                text.setAttribute('text-anchor', value);
            } else if (key === 'fontStyle') {
                text.setAttribute('font-style', value);
            } else {
                text.setAttribute(key, value);
            }
        });
        
        return text;
    }
}

// Export for use in other modules
window.SupermarketMap = SupermarketMap;
