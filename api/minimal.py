from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'status': 'working',
        'message': 'Minimal Flask on Vercel'
    })

# Vercel will automatically detect and use the 'app' object
