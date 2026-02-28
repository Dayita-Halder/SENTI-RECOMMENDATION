#!/usr/bin/env python
"""Quick test of Flask app endpoints."""
import app

if __name__ == '__main__':
    with app.app.test_client() as client:
        # Test health endpoint
        response = client.get('/health')
        print(f"Health: {response.status_code} -> {response.get_json()}")
        
        # Test status endpoint
        response = client.get('/api/status')
        print(f"Status: {response.status_code}")
        
print("✓ All endpoints available")
