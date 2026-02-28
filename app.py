"""
Flask Application for Sentiment-Based Product Recommendation System
===================================================================
Complete web server with routes for sentiment prediction and recommendations.

Endpoints:
- GET / : Serve index.html (user interface)
- POST /api/predict : Sentiment prediction
- POST /api/recommend : Product recommendations
- POST /api/combined : Sentiment + recommendations (complete pipeline)
"""

from flask import Flask, render_template, request, jsonify
import os
import sys
import traceback
from model import get_system, preprocess_text

# ============================================================
# FLASK APPLICATION SETUP
# ============================================================

app = Flask(
    __name__,
    template_folder=os.path.dirname(os.path.abspath(__file__)),
    static_folder=os.path.dirname(os.path.abspath(__file__))
)

# Configuration
app.config['JSON_SORT_KEYS'] = False
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size

# ============================================================
# GLOBAL STATE
# ============================================================

system = None
system_initialized = False

def get_or_init_system():
    """Lazy-initialize system on first use."""
    global system, system_initialized
    if system_initialized:
        return system
    
    system_initialized = True
    try:
        system = get_system()
        print("✓ Sentiment/Recommendation system initialized")
        return system
    except Exception as e:
        print(f"⚠ System initialization deferred (will retry on request): {e}")
        return None


# ============================================================
# ROUTES: HTML & STATIC
# ============================================================

@app.route('/')
def index():
    """Serve the main HTML interface."""
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading interface: {e}", 500


# ============================================================
# ROUTES: API ENDPOINTS
# ============================================================

@app.route('/api/predict', methods=['POST'])
def api_predict_sentiment():
    """
    Predict sentiment for a given review text.
    
    Request JSON:
    {
        "review_text": "This product is amazing!"
    }
    
    Response JSON:
    {
        "sentiment": "Positive",
        "probability": 0.95,
        "confidence": 0.95,
        "success": true
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({'error': 'No JSON data provided', 'success': False}), 400
        
        review_text = data.get('review_text', '').strip()
        
        if not review_text:
            return jsonify({'error': 'Review text is empty', 'success': False}), 400
        
        if len(review_text) > 5000:
            return jsonify({'error': 'Review text too long (max 5000 chars)', 'success': False}), 400
        
        # Predict
        sys = get_or_init_system()
        if sys is None:
            return jsonify({'error': 'System initializing, please retry', 'success': False}), 503
        
        result = sys.predict_sentiment(review_text)
        result['success'] = True
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False,
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/recommend', methods=['POST'])
def api_recommend_products():
    """
    Generate product recommendations for a user.
    
    Request JSON:
    {
        "username": "john_doe",
        "n_recommendations": 5
    }
    
    Response JSON:
    {
        "recommendations": [
            {
                "product": "Product Name",
                "sentiment_score": 0.87,
                "review_count": 42
            },
            ...
        ],
        "explanation": "Recommended based on collaborative filtering + sentiment analysis",
        "is_new_user": false,
        "success": true
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({'error': 'No JSON data provided', 'success': False}), 400
        
        username = data.get('username', '').strip()
        n = data.get('n_recommendations', 5)
        
        if not username:
            return jsonify({'error': 'Username is required', 'success': False}), 400
        
        if len(username) > 50:
            return jsonify({'error': 'Username too long (max 50 chars)', 'success': False}), 400
        
        if not isinstance(n, int) or n < 1 or n > 20:
            n = 5
        
        # Generate recommendations
        sys = get_or_init_system()
        if sys is None:
            return jsonify({'error': 'System initializing, please retry', 'success': False}), 503
        
        result = sys.recommend_products(username, n=n)
        result['success'] = True
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False,
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/combined', methods=['POST'])
def api_predict_and_recommend():
    """
    Complete pipeline: Predict sentiment AND generate recommendations.
    
    Request JSON:
    {
        "username": "john_doe",
        "review_text": "This product is amazing!",
        "n_recommendations": 5
    }
    
    Response JSON:
    {
        "sentiment": "Positive",
        "sentiment_probability": 0.95,
        "sentiment_confidence": 0.95,
        "recommendations": [
            {
                "product": "Product Name",
                "sentiment_score": 0.87,
                "review_count": 42
            },
            ...
        ],
        "recommendation_explanation": "Recommended based on...",
        "is_new_user": false,
        "timestamp": "2026-02-28T12:34:56.789012",
        "success": true
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({'error': 'No JSON data provided', 'success': False}), 400
        
        username = data.get('username', '').strip()
        review_text = data.get('review_text', '').strip()
        n = data.get('n_recommendations', 5)
        
        if not username:
            return jsonify({'error': 'Username is required', 'success': False}), 400
        
        if not review_text:
            return jsonify({'error': 'Review text is required', 'success': False}), 400
        
        if len(username) > 50:
            return jsonify({'error': 'Username too long (max 50 chars)', 'success': False}), 400
        
        if len(review_text) > 5000:
            return jsonify({'error': 'Review text too long (max 5000 chars)', 'success': False}), 400
        
        if not isinstance(n, int) or n < 1 or n > 20:
            n = 5
        
        # Complete pipeline
        sys = get_or_init_system()
        if sys is None:
            return jsonify({'error': 'System initializing, please retry', 'success': False}), 503
        
        result = sys.predict_and_recommend(username, review_text, n_recommendations=n)
        result['success'] = True
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False,
            'traceback': traceback.format_exc()
        }), 500


@app.route('/health')
def health():
    """Simple health check (doesn't load models)."""
    return jsonify({'status': 'healthy', 'service': 'sentiment-recommender'}), 200


@app.route('/api/status')
def api_status():
    """API status check with model info."""
    try:
        sys = get_or_init_system()
        return jsonify({
            'status': 'healthy' if sys else 'initializing',
            'models_loaded': sys is not None
        }), 200 if sys else 202
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found', 'success': False}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({'error': 'Method not allowed', 'success': False}), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error', 'success': False}), 500


# ============================================================
# STARTUP & SHUTDOWN
# ============================================================

@app.before_request
def before_request():
    """Initialize system on first request if needed."""
    if request.path.startswith('/api/'):
        get_or_init_system()


if __name__ == '__main__':
    # Startup banner
    print("="*70)
    print("🚀 SENTIMENT-BASED RECOMMENDATION SYSTEM")
    print("="*70)
    print()
    print("System will initialize on first API request...")
    
    print("\n📡 Starting Flask server...")
    print("="*70)
    print("🌐 Open http://localhost:5000 in your browser")
    print("📊 API Documentation:")
    print("   - POST /api/predict        : Sentiment prediction")
    print("   - POST /api/recommend      : Product recommendations")
    print("   - POST /api/combined       : Sentiment + recommendations")
    print("   - GET  /api/health         : Health check")
    print("="*70)
    print()
    
    # Run Flask app
    app.run(
        host='0.0.0.0',  # Listen on all interfaces for containerized deployment
        port=int(os.environ.get('PORT', 5000)),
        debug=False,
        use_reloader=False
    )
