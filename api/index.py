"""
Vercel Serverless Function for Sentiment-Based Product Recommender
====================================================================
This is the entry point for Vercel deployment.
Routes all API requests through Flask-like endpoints using Vercel functions.
"""

import os
import sys
import json
import traceback
from urllib.parse import parse_qs

# Add parent directory to path to import model.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from model import get_system, preprocess_text
    SYSTEM_AVAILABLE = True
except Exception as e:
    print(f"Warning: Could not import model: {e}")
    SYSTEM_AVAILABLE = False

# ============================================================
# GLOBAL STATE
# ============================================================

system = None

def initialize_system():
    """Initialize the ML system on first request."""
    global system
    if system is None and SYSTEM_AVAILABLE:
        try:
            system = get_system()
            return True
        except Exception as e:
            print(f"Error initializing system: {e}")
            return False
    return SYSTEM_AVAILABLE


# ============================================================
# RESPONSE HELPERS
# ============================================================

def json_response(data, status_code=200):
    """Return a JSON response with proper headers."""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
        'body': json.dumps(data)
    }


def error_response(message, status_code=400):
    """Return an error response."""
    return json_response({
        'error': message,
        'success': False
    }, status_code)


# ============================================================
# API HANDLERS
# ============================================================

def handle_predict(data):
    """
    Handle POST /api/predict
    Predict sentiment for a review.
    """
    if not system:
        return error_response('System not initialized', 500)
    
    review_text = data.get('review_text', '').strip()
    
    if not review_text:
        return error_response('Review text is required', 400)
    
    if len(review_text) > 5000:
        return error_response('Review text too long (max 5000 chars)', 400)
    
    try:
        result = system.predict_sentiment(review_text)
        result['success'] = True
        return json_response(result)
    except Exception as e:
        return error_response(f'Prediction error: {str(e)}', 500)


def handle_recommend(data):
    """
    Handle POST /api/recommend
    Generate product recommendations for a user.
    """
    if not system:
        return error_response('System not initialized', 500)
    
    username = data.get('username', '').strip()
    n = data.get('n_recommendations', 5)
    
    if not username:
        return error_response('Username is required', 400)
    
    if len(username) > 50:
        return error_response('Username too long (max 50 chars)', 400)
    
    if not isinstance(n, int) or n < 1 or n > 20:
        n = 5
    
    try:
        result = system.recommend_products(username, n=n)
        result['success'] = True
        return json_response(result)
    except Exception as e:
        return error_response(f'Recommendation error: {str(e)}', 500)


def handle_combined(data):
    """
    Handle POST /api/combined
    Complete pipeline: predict sentiment AND generate recommendations.
    """
    if not system:
        return error_response('System not initialized', 500)
    
    username = data.get('username', '').strip()
    review_text = data.get('review_text', '').strip()
    n = data.get('n_recommendations', 5)
    
    if not username:
        return error_response('Username is required', 400)
    
    if not review_text:
        return error_response('Review text is required', 400)
    
    if len(username) > 50:
        return error_response('Username too long (max 50 chars)', 400)
    
    if len(review_text) > 5000:
        return error_response('Review text too long (max 5000 chars)', 400)
    
    if not isinstance(n, int) or n < 1 or n > 20:
        n = 5
    
    try:
        result = system.predict_and_recommend(username, review_text, n_recommendations=n)
        result['success'] = True
        return json_response(result)
    except Exception as e:
        return error_response(f'Pipeline error: {str(e)}', 500)


def handle_health(data):
    """
    Handle GET /api/health
    Health check endpoint.
    """
    if not system:
        return json_response({
            'status': 'error',
            'message': 'System not initialized',
            'system_ready': False
        }, 500)
    
    try:
        # Quick test
        test_result = system.predict_sentiment("test")
        return json_response({
            'status': 'healthy',
            'message': 'Sentiment/Recommendation system is operational',
            'system_ready': True
        })
    except Exception as e:
        return json_response({
            'status': 'error',
            'message': str(e),
            'system_ready': False
        }, 500)


# ============================================================
# MAIN HANDLER
# ============================================================

def handler(event, context):
    """
    Vercel serverless function handler.
    Entry point for all requests.
    
    Args:
        event: HTTP event from Vercel (path, method, body, etc.)
        context: Vercel context object
        
    Returns:
        dict with statusCode, headers, body
    """
    
    # Initialize system on first request
    initialize_system()
    
    # Parse request
    method = event.get('httpMethod', 'GET').upper()
    path = event.get('path', '/').lower()
    
    # Handle CORS pre-flight
    if method == 'OPTIONS':
        return json_response({}, 200)
    
    # Parse body
    body_str = event.get('body', '{}')
    if isinstance(body_str, str):
        try:
            body = json.loads(body_str) if body_str else {}
        except json.JSONDecodeError:
            body = {}
    else:
        body = body_str
    
    # Route requests
    try:
        if path == '/api/predict' and method == 'POST':
            return handle_predict(body)
        
        elif path == '/api/recommend' and method == 'POST':
            return handle_recommend(body)
        
        elif path == '/api/combined' and method == 'POST':
            return handle_combined(body)
        
        elif path == '/api/health' and method == 'GET':
            return handle_health(body)
        
        else:
            return error_response(f'Endpoint not found: {method} {path}', 404)
    
    except Exception as e:
        return error_response(f'Internal error: {str(e)}', 500)
