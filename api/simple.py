import json

def handler(event, context):
    """Vercel serverless function handler."""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'status': 'ok',
            'message': 'Vercel Python function working!',
            'event_keys': list(event.keys()) if isinstance(event, dict) else str(type(event))
        })
    }
