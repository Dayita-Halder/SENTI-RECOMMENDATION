"""
Minimal test endpoint - no dependencies
"""

def handler(request, context):
    """Absolute minimal handler for testing."""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': '{"status": "ok", "message": "Minimal endpoint working"}'
    }
