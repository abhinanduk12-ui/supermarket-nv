# 🏪 Supermarket 2D Navigator

A professional, full-stack indoor navigation system for supermarkets that uses **Dijkstra's shortest-path algorithm** to find optimal routes between products. Built with Python Flask backend, REST API, and an interactive SVG-based map visualization.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### Core Functionality
- **🔍 Intelligent Product Search** - Search through 60+ products across 13 categories
- **🎯 Shortest Path Calculation** - Real Dijkstra's algorithm implementation
- **🗺️ Interactive SVG Map** - Professional floor plan with zoom and pan
- **📍 Real-time Navigation** - Animated route visualization with step-by-step instructions
- **⚡ Fast REST API** - Clean Flask backend with modular architecture

### User Experience
- **🎨 Premium Olive Green Design** - Modern, elegant UI/UX
- **📱 Fully Responsive** - Works on desktop, tablet, and mobile
- **✨ Smooth Animations** - Polished micro-interactions throughout
- **♿ Accessible** - WCAG compliant with keyboard navigation
- **🎭 Reduced Motion Support** - Respects user accessibility preferences

### Technical Highlights
- **Graph-based Navigation** - 24 nodes with weighted edges
- **Real Algorithm** - Actual Dijkstra implementation (not hardcoded routes)
- **Clean Architecture** - Modular backend with service layers
- **Comprehensive Tests** - Unit tests for algorithm and API
- **Professional Code** - Type hints, docstrings, and best practices

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the repository**
```bash
cd supermarket-2d-navigator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Open your browser**
```
http://localhost:5001
```

That's it! The application should now be running.

## 📖 How to Use

1. **Search for a Product**
   - Type in the search box (e.g., "milk", "bread", "rice")
   - Select a product from the dropdown results

2. **Select Starting Point**
   - Choose your starting location (Entrance, Checkout, etc.)

3. **Find Route**
   - Click "Find Shortest Route"
   - Watch the animated route appear on the map

4. **Follow Instructions**
   - Read step-by-step navigation instructions
   - View distance, time, and number of steps

5. **Reset and Search Again**
   - Click "Reset Navigation" to start over

## 🏗️ Project Structure

```
supermarket-2d-navigator/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── backend/                        # Backend package
│   ├── algorithms/                 # Algorithm implementations
│   │   └── dijkstra.py            # Dijkstra's shortest path
│   │
│   ├── routes/                     # API endpoints
│   │   ├── products.py            # Product routes
│   │   └── navigation.py          # Navigation routes
│   │
│   ├── services/                   # Business logic
│   │   ├── product_service.py     # Product operations
│   │   └── navigation_service.py  # Navigation operations
│   │
│   └── data/                       # Data storage
│       ├── products.json          # Product database (60 items)
│       └── graph.json             # Supermarket graph structure
│
├── templates/                      # HTML templates
│   └── index.html                 # Main application page
│
├── static/                         # Static assets
│   ├── css/
│   │   └── style.css              # Complete styling (900+ lines)
│   │
│   └── js/
│       ├── app.js                 # Main application logic
│       ├── map.js                 # SVG map & interactions
│       ├── search.js              # Search functionality
│       └── navigation.js          # Route calculation
│
└── tests/                          # Unit tests
    ├── test_dijkstra.py           # Algorithm tests
    └── test_api.py                # API endpoint tests
```

## 🔧 Technology Stack

### Backend
- **Python 3** - Core programming language
- **Flask 3.0** - Web framework
- **Flask-CORS** - Cross-origin resource sharing
- **JSON** - Data storage (easily upgradeable to database)

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with animations
- **Vanilla JavaScript** - No frameworks, pure JS
- **SVG** - Vector graphics for interactive map

### Algorithms
- **Dijkstra's Algorithm** - Shortest path calculation
- **Graph Theory** - Network representation

## 🧪 Running Tests

### Run all tests
```bash
python -m pytest tests/
```

### Run specific test file
```bash
python -m unittest tests/test_dijkstra.py
python -m unittest tests/test_api.py
```

### Test coverage
The test suite includes:
- ✅ Algorithm correctness tests
- ✅ Edge case handling
- ✅ API endpoint tests
- ✅ Error handling tests
- ✅ Performance tests

## 🎨 Design System

### Color Palette
- **Primary Olive**: `#667A3E` - Main brand color
- **Deep Olive**: `#3F4D27` - Headers and emphasis
- **Soft Sage**: `#DCE5C5` - Subtle backgrounds
- **Cream**: `#F7F5EC` - Light backgrounds
- **Warm White**: `#FCFCF8` - Main background
- **Charcoal**: `#20251B` - Primary text

### Typography
- **System Font Stack** - Native, optimized fonts
- **Font Weights**: 400 (regular), 600 (semibold), 700 (bold), 800 (extrabold)

### Components
- Modern card-based layouts
- Smooth transitions and animations
- Professional spacing and hierarchy
- Accessible focus states

## 📊 Graph Structure

### Nodes (24 total)
- **Entrance** - Main entry point
- **Checkout Area** - Payment zone
- **Customer Service** - Help desk
- **Junctions** - Path intersections
- **Aisles** - Product locations (4 aisles × 3 sections)

### Edges
- Weighted by walking distance in meters
- Bidirectional connections
- Optimized for realistic navigation

### Example Route
```
Entrance (10m) → Junction 1 (20m) → Junction 2 (5m) → Aisle 2 Middle
Total: 35 meters, ~25 seconds walking time
```

## 🚦 API Documentation

### Products

#### Get All Products
```http
GET /api/products
```

#### Search Products
```http
GET /api/products/search?q=milk
```

#### Get Product by ID
```http
GET /api/products/P001
```

### Navigation

#### Calculate Route
```http
POST /api/route
Content-Type: application/json

{
  "start": "entrance",
  "destination": "aisle_1_mid"
}
```

#### Get Graph Nodes
```http
GET /api/graph/nodes
```

#### Get Graph Edges
```http
GET /api/graph/edges
```

### Health Check
```http
GET /api/health
```

## 🎯 Key Features Explained

### Dijkstra's Algorithm
The navigation system uses a proper implementation of Dijkstra's algorithm:
1. Initializes distances to infinity
2. Uses a priority queue (heapq)
3. Explores nodes in order of distance
4. Updates distances when shorter paths are found
5. Reconstructs the path from destination to start
6. Returns the optimal route

### Route Animation
- Animated dashed line showing the path
- Moving marker that travels along the route
- Pulsing destination marker
- Smooth transitions and easing

### Search Features
- Real-time search with debouncing (300ms)
- Matches product name, category, and aisle
- Instant results display
- Clear visual feedback

## 🔐 Security Considerations

- Input validation on all API endpoints
- Error handling without exposing stack traces
- CORS configuration for API access
- No sensitive data in client-side code

## 🚀 Future Enhancements

Potential improvements for the project:

- [ ] Multi-product route optimization
- [ ] Real-time product availability
- [ ] Shopping list management
- [ ] Voice navigation
- [ ] AR overlay for mobile
- [ ] Admin panel for product management
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User accounts and preferences
- [ ] Multiple supermarket layouts
- [ ] Analytics dashboard

## 🤝 Contributing

This is a portfolio project, but suggestions and improvements are welcome!

## 📄 License

MIT License - Feel free to use this project for learning or portfolio purposes.

## 👨‍💻 Developer Notes

### Code Quality
- Clean, readable code with proper naming
- Comprehensive comments and docstrings
- Modular architecture for maintainability
- Follows Python PEP 8 style guidelines
- Professional JavaScript practices

### Browser Compatibility
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

### Performance
- Optimized SVG rendering
- Efficient graph algorithms
- Debounced search
- Lazy loading where appropriate

## 📞 Support

For questions or issues:
1. Check the documentation above
2. Review the code comments
3. Run the test suite
4. Inspect browser console for errors

## 🎓 Educational Value

This project demonstrates:
- **Data Structures**: Graphs, priority queues
- **Algorithms**: Dijkstra's shortest path
- **Web Development**: Full-stack application
- **API Design**: RESTful architecture
- **Frontend**: Interactive visualizations
- **Software Engineering**: Clean code, testing, documentation

Perfect for:
- Software engineering portfolios
- Computer science projects
- Learning graph algorithms
- Full-stack development practice

---

**Built with ❤️ using Python, Flask, and Dijkstra's Algorithm**

*A professional portfolio project demonstrating full-stack development and computer science fundamentals*
