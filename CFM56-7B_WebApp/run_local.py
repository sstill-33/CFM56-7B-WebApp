#!/usr/bin/env python3
"""
Run the CFM56-7B web application locally for testing
"""

from app import app
import socket

def find_free_port():
    """Find a free port starting from 5001"""
    for port in range(5001, 5100):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return 8080  # Fallback port

if __name__ == '__main__':
    port = find_free_port()
    print("=== CFM56-7B Web Application ===")
    print("Starting local development server...")
    print(f"Open your browser and go to: http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=port)
