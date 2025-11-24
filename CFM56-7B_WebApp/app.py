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
    # Try multiple possible paths for Railway deployment
    possible_paths = [
        'data/pdf_linked_database.json',
        'CFM56-7B_WebApp/data/pdf_linked_database.json',
        os.path.join(os.path.dirname(__file__), 'data', 'pdf_linked_database.json')
    ]
    
    for db_path in possible_paths:
        try:
            if os.path.exists(db_path):
                with open(db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            continue
    
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

if __name__ == '__main__':
    # Railway provides PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    # Disable debug mode in production
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
