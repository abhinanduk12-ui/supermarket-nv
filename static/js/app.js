/**
 * Main Application Module
 * Initializes and coordinates all modules
 */

// Global instances
let mapInstance = null;
let searchInstance = null;
let navigationInstance = null;

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('🏪 Supermarket 2D Navigator - Initializing...');
    
    initializeApplication();
    setupScrollHandlers();
    setupAnimations();
    
    console.log('✅ Application initialized successfully');
});

/**
 * Initialize all application modules
 */
function initializeApplication() {
    // Initialize map
    mapInstance = new SupermarketMap('map-wrapper');
    window.mapInstance = mapInstance;
    
    // Initialize search
    searchInstance = new ProductSearch();
    window.searchInstance = searchInstance;
    
    // Initialize navigation
    navigationInstance = new NavigationController(searchInstance, mapInstance);
    window.navigationInstance = navigationInstance;
}

/**
 * Setup scroll handlers for smooth navigation
 */
function setupScrollHandlers() {
    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Setup animations and micro-interactions
 */
function setupAnimations() {
    // Animate stats counter on hero section
    animateStatsCounters();
    
    // Setup intersection observer for fade-in animations
    setupIntersectionObserver();
    
    // Add hover effects to cards
    setupCardHoverEffects();
}

/**
 * Animate statistics counters in hero section
 */
function animateStatsCounters() {
    const statValues = document.querySelectorAll('.stat-value');
    
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.dataset.target);
                animateCounter(entry.target, 0, target, 1500);
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    statValues.forEach(stat => observer.observe(stat));
}

/**
 * Animate a counter from start to end value
 */
function animateCounter(element, start, end, duration) {
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function
        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
        const current = Math.floor(start + (end - start) * easeOutQuart);
        
        element.textContent = current;
        
        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            element.textContent = end;
        }
    }
    
    requestAnimationFrame(update);
}

/**
 * Setup intersection observer for scroll animations
 */
function setupIntersectionObserver() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe step cards
    document.querySelectorAll('.step-card').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `all 0.6s ease-out ${index * 0.1}s`;
        observer.observe(card);
    });
    
    // Observe tech badges
    document.querySelectorAll('.tech-badge').forEach((badge, index) => {
        badge.style.opacity = '0';
        badge.style.transform = 'translateY(20px)';
        badge.style.transition = `all 0.4s ease-out ${index * 0.05}s`;
        observer.observe(badge);
    });
}

/**
 * Setup hover effects for cards
 */
function setupCardHoverEffects() {
    const cards = document.querySelectorAll('.step-card, .tech-badge, .stat-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
        });
    });
}

/**
 * Scroll to navigator section
 */
function scrollToNavigator() {
    const navigatorSection = document.getElementById('navigator');
    if (navigatorSection) {
        navigatorSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

/**
 * Scroll to map
 */
function scrollToMap() {
    const mapWrapper = document.getElementById('map-wrapper');
    if (mapWrapper) {
        mapWrapper.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    }
}

/**
 * Handle navbar background on scroll
 */
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
    
    lastScroll = currentScroll;
});

/**
 * Handle window resize
 */
let resizeTimer;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        console.log('Window resized, adjusting layout...');
        if (mapInstance) {
            mapInstance.resetView();
        }
    }, 250);
});

/**
 * Check for reduced motion preference
 */
function prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

if (prefersReducedMotion()) {
    console.log('⚠️ Reduced motion preference detected');
    document.documentElement.style.setProperty('--transition-fast', '0ms');
    document.documentElement.style.setProperty('--transition-base', '0ms');
    document.documentElement.style.setProperty('--transition-slow', '0ms');
}

/**
 * Error handler for uncaught errors
 */
window.addEventListener('error', (event) => {
    console.error('Application error:', event.error);
});

/**
 * Service worker registration (for future PWA support)
 */
if ('serviceWorker' in navigator) {
    // Service worker can be added later for offline support
    console.log('Service Worker API available');
}

// Export utility functions to global scope
window.scrollToNavigator = scrollToNavigator;
window.scrollToMap = scrollToMap;

// Log initialization complete
console.log(`
╔═══════════════════════════════════════════╗
║   Supermarket 2D Navigator - Ready!      ║
║   Built with Flask + Dijkstra Algorithm  ║
╚═══════════════════════════════════════════╝
`);
