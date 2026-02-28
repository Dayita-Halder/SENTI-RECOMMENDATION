"""
Vercel Serverless Function for Sentiment-Based Product Recommender
====================================================================
Flask-based API for Vercel deployment.
"""

import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS

try:
    from model import get_system
    SYSTEM_AVAILABLE = True
    IMPORT_ERROR = None
except Exception as e:
    SYSTEM_AVAILABLE = False
    IMPORT_ERROR = str(e)
    print(f"Warning: Could not import model: {e}")
    traceback.print_exc()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global system instance
system = None
system_init_error = None

def get_or_create_system():
    """Get or initialize the ML system."""
    global system, system_init_error
    if system is None and SYSTEM_AVAILABLE:
        try:
            system = get_system()
            system_init_error = None
        except Exception as e:
            system_init_error = str(e)
            print(f"Error initializing system: {e}")
            traceback.print_exc()
            return None
    return system

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    sys_instance = get_or_create_system()
    return jsonify({
        'status': 'healthy' if sys_instance else 'unhealthy',
        'system_available': SYSTEM_AVAILABLE,
        'system_loaded': sys_instance is not None,
        'init_error': system_init_error,
        'import_error': IMPORT_ERROR
    }), (200 if sys_instance else 500)

@app.route('/predict', methods=['POST'])
def predict():
    """Predict sentiment for a review."""
    sys_instance = get_or_create_system()
    if not sys_instance:
        return jsonify({'error': 'System not initialized', 'success': False}), 500
    
    data = request.get_json()
    review_text = data.get('review_text', '').strip()
    
    if not review_text:
        return jsonify({'error': 'Review text is required', 'success': False}), 400
    
    if len(review_text) > 5000:
        return jsonify({'error': 'Review text too long (max 5000 chars)', 'success': False}), 400
    
    try:
        result = sys_instance.predict_sentiment(review_text)
        result['success'] = True
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Prediction error: {str(e)}', 'success': False}), 500

@app.route('/recommend', methods=['POST'])
def recommend():
    """Generate product recommendations."""
    sys_instance = get_or_create_system()
    if not sys_instance:
        return jsonify({'error': 'System not initialized', 'success': False}), 500
    
    data = request.get_json()
    username = data.get('username', '').strip()
    n_recommendations = data.get('n_recommendations', 5)
    
    if not username:
        return jsonify({'error': 'Username is required', 'success': False}), 400
    
    try:
        n_recommendations = int(n_recommendations)
        if n_recommendations < 1 or n_recommendations > 20:
            return jsonify({'error': 'n_recommendations must be between 1 and 20', 'success': False}), 400
    except ValueError:
        return jsonify({'error': 'Invalid n_recommendations', 'success': False}), 400
    
    try:
        recommendations = sys_instance.recommend_products(username, n_recommendations)
        return jsonify({
            'success': True,
            'username': username,
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({'error': f'Recommendation error: {str(e)}', 'success': False}), 500

@app.route('/combined', methods=['POST'])
def combined():
    """Combined sentiment prediction and recommendations."""
    sys_instance = get_or_create_system()
    if not sys_instance:
        return jsonify({'error': 'System not initialized', 'success': False}), 500
    
    data = request.get_json()
    username = data.get('username', '').strip()
    review_text = data.get('review_text', '').strip()
    n_recommendations = data.get('n_recommendations', 5)
    
    if not username:
        return jsonify({'error': 'Username is required', 'success': False}), 400
    
    if not review_text:
        return jsonify({'error': 'Review text is required', 'success': False}), 400
    
    if len(review_text) > 5000:
        return jsonify({'error': 'Review text too long (max 5000 chars)', 'success': False}), 400
    
    try:
        n_recommendations = int(n_recommendations)
        if n_recommendations < 1 or n_recommendations > 20:
            return jsonify({'error': 'n_recommendations must be between 1 and 20', 'success': False}), 400
    except ValueError:
        return jsonify({'error': 'Invalid n_recommendations', 'success': False}), 400
    
    try:
        result = sys_instance.predict_and_recommend(username, review_text, n_recommendations)
        result['success'] = True
        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'Error: {str(e)}', 'success': False}), 500

# Export for Vercel
handler = app
