"""
Health check endpoint for Vercel
"""
import json
import sys
import os

# Add the api directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def handler(request, context):
    """Simple health check that doesn't require model loading."""
    
    response_body = {
        'status': 'healthy',
        'python_version': sys.version,
        'sys_path': sys.path[:3],
        'cwd': os.getcwd(),
        'api_dir': os.path.dirname(os.path.abspath(__file__)),
        'pickle_files_exist': False
    }
    
    # Check if pickle directory exists
    pickle_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pickle')
    if os.path.exists(pickle_dir):
        pickle_files = os.listdir(pickle_dir)
        response_body['pickle_files_exist'] = True
        response_body['pickle_files'] = pickle_files
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(response_body)
    }
