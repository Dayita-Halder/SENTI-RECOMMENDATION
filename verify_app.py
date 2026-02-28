#!/usr/bin/env python
"""Test if Flask app is valid."""
from app import app

print("✓ Flask app loaded successfully")
print("\nRegistered routes:")
for rule in app.url_map.iter_rules():
    print(f"  {rule.rule} -> {rule.endpoint} {rule.methods}")

print("\nTesting /health endpoint:")
with app.test_client() as client:
    response = client.get('/health')
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.get_json()}")
