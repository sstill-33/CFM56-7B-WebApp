#!/usr/bin/env python3
"""
CFM56-7B Aviation Maintenance Search System
Flask Web Application for PythonAnywhere
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import glob
from pathlib import Path

app = Flask(__name__)

# Load the search database
def load_database():
    """Load the search database"""
    # Get the base directory (where app.py is located)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try multiple possible paths for Railway deployment
    possible_paths = [
        os.path.join(base_dir, 'data', 'pdf_linked_database.json'),  # Relative to app.py
        'data/pdf_linked_database.json',  # Current working directory
        'CFM56-7B_WebApp/data/pdf_linked_database.json',  # From repo root
        os.path.join(os.getcwd(), 'CFM56-7B_WebApp', 'data', 'pdf_linked_database.json'),  # Absolute from cwd
    ]
    
    for db_path in possible_paths:
        try:
            if os.path.exists(db_path):
                print(f"Loading database from: {db_path}")
                with open(db_path, 'r', encoding='utf-8') as f:
                    db = json.load(f)
                    print(f"Database loaded successfully. Parts: {len(db.get('parts', []))}, Documents: {len(db.get('documents', []))}")
                    return db
            else:
                print(f"Database not found at: {db_path}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading database from {db_path}: {e}")
            continue
    
    # Log warning if database not found
    print("WARNING: Database file not found in any of the expected locations!")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Base directory: {base_dir}")
    print(f"Looking for: pdf_linked_database.json")
    
    # Return empty database if file not found
    return {
        'parts': [],
        'documents': [],
        'categories': {},
        'stats': {'total_parts': 0, 'total_documents': 0, 'total_categories': 0}
    }

@app.route('/')
def index():
    """Main search page"""
    database = load_database()
    return render_template('search.html', database=database)

@app.route('/api/search')
def api_search():
    """API endpoint for search"""
    query = request.args.get('q', '').lower()
    category = request.args.get('category', 'all')
    
    if len(query) < 2:
        return jsonify({'results': []})
    
    database = load_database()
    results = []
    
    # Search parts
    for part in database.get('parts', []):
        if category != 'all' and part.get('category') != category:
            continue
            
        # Search in part number, description, or document title
        if (part.get('part_number', '').lower().find(query) != -1 or
            part.get('description', '').lower().find(query) != -1 or
            part.get('document_title', '').lower().find(query) != -1):
            
            # Get actions for this part
            actions = []
            if part.get('pdf_file'):
                actions.append({
                    'text': 'View PDF Document',
                    'url': f'/api/file?path={part["pdf_file"]}',
                    'class': 'pdf'
                })
            if part.get('image_file'):
                actions.append({
                    'text': 'View Image',
                    'url': f'/api/file?path={part["image_file"]}',
                    'class': 'image'
                })
            if part.get('source_file'):
                actions.append({
                    'text': 'View Source XML',
                    'url': f'/api/file?path={part["source_file"]}',
                    'class': 'xml'
                })
            
            results.append({
                'document_title': part.get('document_title', 'Unknown Document'),
                'part_number': part.get('part_number', 'N/A'),
                'description': part.get('description', 'No description available'),
                'details': f"Category: {part.get('category', 'Unknown')} | Chapter: {part.get('chapter', '')}-{part.get('section', '')}-{part.get('unit', '')} | Figure: {part.get('figure', '')}",
                'category': part.get('category', 'Unknown'),
                'actions': actions
            })
    
    return jsonify({'results': results})

@app.route('/api/file')
def api_file():
    """Serve files (PDFs, images, etc.)"""
    file_path = request.args.get('path', '')
    if not file_path or not os.path.exists(file_path):
        return "File not found", 404
    
    return send_file(file_path)

@app.route('/api/stats')
def api_stats():
    """Get database statistics"""
    database = load_database()
    return jsonify(database.get('stats', {}))

@app.route('/api/debug')
def api_debug():
    """Debug endpoint to check database file locations"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cwd = os.getcwd()
    
    possible_paths = [
        os.path.join(base_dir, 'data', 'pdf_linked_database.json'),
        'data/pdf_linked_database.json',
        'CFM56-7B_WebApp/data/pdf_linked_database.json',
        os.path.join(os.getcwd(), 'CFM56-7B_WebApp', 'data', 'pdf_linked_database.json'),
    ]
    
    path_status = {}
    for path in possible_paths:
        exists = os.path.exists(path)
        path_status[path] = {
            'exists': exists,
            'size': os.path.getsize(path) if exists else 0
        }
    
    database = load_database()
    has_data = len(database.get('parts', [])) > 0
    
    return jsonify({
        'current_working_directory': cwd,
        'base_directory': base_dir,
        'path_checks': path_status,
        'database_loaded': has_data,
        'parts_count': len(database.get('parts', [])),
        'documents_count': len(database.get('documents', []))
    })

if __name__ == '__main__':
    # Railway provides PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    # Disable debug mode in production
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
