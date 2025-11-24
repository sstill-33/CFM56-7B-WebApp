#!/usr/bin/env python3
"""
Create a complete web application package for PythonAnywhere hosting
Converts the CFM56-7B search system into a deployable web app
"""

import os
import json
import shutil
import glob
from pathlib import Path

def create_webapp_structure():
    """Create the web application structure for PythonAnywhere"""
    base_dir = "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B"
    webapp_dir = f"{base_dir}/CFM56-7B_WebApp"
    
    print("=== Creating CFM56-7B Web Application Package ===")
    print(f"Creating webapp directory: {webapp_dir}")
    
    # Create main directories
    os.makedirs(webapp_dir, exist_ok=True)
    os.makedirs(f"{webapp_dir}/static", exist_ok=True)
    os.makedirs(f"{webapp_dir}/templates", exist_ok=True)
    os.makedirs(f"{webapp_dir}/data", exist_ok=True)
    
    return webapp_dir

def create_flask_app(webapp_dir):
    """Create the Flask application"""
    app_content = '''#!/usr/bin/env python3
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
    try:
        with open('data/pdf_linked_database.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
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
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
    
    with open(f"{webapp_dir}/app.py", "w", encoding="utf-8") as f:
        f.write(app_content)
    
    print("✅ Flask application created")

def create_html_template(webapp_dir):
    """Create the HTML template"""
    template_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CFM56-7B Aviation Maintenance Search System</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        .search-section {
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
        }
        .search-container {
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 15px;
            margin-bottom: 20px;
        }
        .search-input {
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        .search-input:focus {
            outline: none;
            border-color: #2a5298;
        }
        .search-button {
            padding: 15px 30px;
            background: #2a5298;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .search-button:hover {
            background: #1e3c72;
        }
        .filter-section {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }
        .filter-button {
            padding: 8px 16px;
            background: #f8f9fa;
            border: 1px solid #ddd;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .filter-button.active {
            background: #2a5298;
            color: white;
        }
        .results-section {
            padding: 30px;
        }
        .result-item {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            transition: box-shadow 0.3s;
        }
        .result-item:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .result-title {
            font-size: 1.3em;
            font-weight: 600;
            color: #2a5298;
            margin-bottom: 5px;
            text-decoration: none;
            display: block;
        }
        .result-title:hover {
            color: #1e3c72;
            text-decoration: underline;
        }
        .result-part-number {
            color: #666;
            font-size: 1em;
            margin-bottom: 10px;
            font-weight: 500;
        }
        .result-description {
            color: #333;
            margin-bottom: 10px;
            font-size: 1.1em;
        }
        .result-details {
            color: #666;
            margin-bottom: 15px;
            font-size: 0.9em;
        }
        .result-actions {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .action-button {
            padding: 8px 16px;
            background: #f8f9fa;
            border: 1px solid #ddd;
            border-radius: 4px;
            text-decoration: none;
            color: #333;
            font-size: 0.9em;
            transition: all 0.3s;
        }
        .action-button:hover {
            background: #2a5298;
            color: white;
        }
        .action-button.pdf {
            background: #dc3545;
            color: white;
            border-color: #dc3545;
        }
        .action-button.pdf:hover {
            background: #c82333;
        }
        .action-button.image {
            background: #28a745;
            color: white;
            border-color: #28a745;
        }
        .action-button.image:hover {
            background: #218838;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 20px;
            background: #f8f9fa;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #2a5298;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
        .no-results {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        .category-badge {
            display: inline-block;
            padding: 4px 8px;
            background: #e3f2fd;
            color: #1976d2;
            border-radius: 4px;
            font-size: 0.8em;
            margin-right: 8px;
        }
        .loading {
            text-align: center;
            padding: 20px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>CFM56-7B Aviation Maintenance Search System</h1>
            <p>Search across all document categories with direct PDF access</p>
        </div>
        
        <div class="stats" id="stats">
            <div class="stat-card">
                <div class="stat-number">{{ database.stats.total_parts }}</div>
                <div class="stat-label">Parts & References</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ database.stats.total_documents }}</div>
                <div class="stat-label">PDF Documents</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ database.stats.total_categories }}</div>
                <div class="stat-label">Categories</div>
            </div>
        </div>
        
        <div class="search-section">
            <div class="search-container">
                <input type="text" id="searchInput" class="search-input" placeholder="Search parts, procedures, or any reference..." onkeyup="handleSearch()">
                <button onclick="performSearch()" class="search-button">Search All Categories</button>
            </div>
            
            <div class="filter-section">
                <div class="filter-button active" onclick="filterByCategory('all')">All Categories</div>
                <div class="filter-button" onclick="filterByCategory('EIPC')">EIPC</div>
                <div class="filter-button" onclick="filterByCategory('ESM')">ESM</div>
                <div class="filter-button" onclick="filterByCategory('SB')">SB</div>
                <div class="filter-button" onclick="filterByCategory('CMM')">CMM</div>
                <div class="filter-button" onclick="filterByCategory('CPM')">CPM</div>
                <div class="filter-button" onclick="filterByCategory('ITEM')">ITEM</div>
                <div class="filter-button" onclick="filterByCategory('NDTM')">NDTM</div>
                <div class="filter-button" onclick="filterByCategory('LLP')">LLP</div>
                <div class="filter-button" onclick="filterByCategory('SOLUTIONS')">SOLUTIONS</div>
                <div class="filter-button" onclick="filterByCategory('SPM')">SPM</div>
                <div class="filter-button" onclick="filterByCategory('TSP')">TSP</div>
            </div>
        </div>
        
        <div class="results-section">
            <div id="searchResults">
                <div class="no-results">
                    <h3>Search with direct PDF access</h3>
                    <p>Enter a search term to find parts, procedures, or references with direct links to PDF documents</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentFilter = 'all';
        
        function handleSearch() {
            const query = document.getElementById('searchInput').value.trim();
            if (query.length >= 2) {
                performSearch();
            } else {
                showNoResults();
            }
        }
        
        function filterByCategory(category) {
            currentFilter = category;
            
            // Update filter buttons
            document.querySelectorAll('.filter-button').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Re-run search if there's a query
            const query = document.getElementById('searchInput').value.trim();
            if (query.length >= 2) {
                performSearch();
            }
        }
        
        function performSearch() {
            const query = document.getElementById('searchInput').value.trim();
            if (query.length < 2) {
                showNoResults();
                return;
            }
            
            // Show loading
            document.getElementById('searchResults').innerHTML = '<div class="loading">Searching...</div>';
            
            // Make API call
            fetch(`/api/search?q=${encodeURIComponent(query)}&category=${currentFilter}`)
                .then(response => response.json())
                .then(data => {
                    displayResults(data.results);
                })
                .catch(error => {
                    console.error('Search error:', error);
                    showNoResults();
                });
        }
        
        function displayResults(results) {
            const resultsContainer = document.getElementById('searchResults');
            
            if (results.length === 0) {
                showNoResults();
                return;
            }
            
            let html = '';
            results.forEach(result => {
                const pdfAction = result.actions.find(a => a.class === 'pdf');
                const titleLink = pdfAction ? pdfAction.url : '#';
                
                html += `
                    <div class="result-item">
                        <a href="${titleLink}" class="result-title" target="_blank">
                            ${result.document_title}
                            <span class="category-badge">${result.category}</span>
                        </a>
                        <div class="result-part-number">Part/Keyword: ${result.part_number}</div>
                        <div class="result-description">${result.description}</div>
                        <div class="result-details">${result.details}</div>
                        <div class="result-actions">
                            ${result.actions.map(action => 
                                `<a href="${action.url}" class="action-button ${action.class || ''}" target="_blank">${action.text}</a>`
                            ).join('')}
                        </div>
                    </div>
                `;
            });
            
            resultsContainer.innerHTML = html;
        }
        
        function showNoResults() {
            const resultsContainer = document.getElementById('searchResults');
            resultsContainer.innerHTML = `
                <div class="no-results">
                    <h3>No results found</h3>
                    <p>Try searching for part numbers, keywords, or document titles</p>
                </div>
            `;
        }
    </script>
</body>
</html>'''
    
    with open(f"{webapp_dir}/templates/search.html", "w", encoding="utf-8") as f:
        f.write(template_content)
    
    print("✅ HTML template created")

def copy_database(webapp_dir):
    """Copy the search database to the webapp"""
    source_db = "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B_Extracted/pdf_linked_database.json"
    target_db = f"{webapp_dir}/data/pdf_linked_database.json"
    
    if os.path.exists(source_db):
        shutil.copy2(source_db, target_db)
        print("✅ Database copied to webapp")
    else:
        print("⚠️  Database not found, creating empty one")
        empty_db = {
            'parts': [],
            'documents': [],
            'categories': {},
            'stats': {'total_parts': 0, 'total_documents': 0, 'total_categories': 0}
        }
        with open(target_db, 'w', encoding='utf-8') as f:
            json.dump(empty_db, f, indent=2)

def create_requirements_file(webapp_dir):
    """Create requirements.txt for PythonAnywhere"""
    requirements = """Flask==2.3.3
Werkzeug==2.3.7
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
blinker==1.6.2"""
    
    with open(f"{webapp_dir}/requirements.txt", "w") as f:
        f.write(requirements)
    
    print("✅ Requirements file created")

def create_deployment_guide(webapp_dir):
    """Create deployment guide for PythonAnywhere"""
    guide_content = """# CFM56-7B Web Application Deployment Guide

## PythonAnywhere Deployment Instructions

### 1. Upload Files
1. Go to PythonAnywhere.com and create an account
2. Upload all files from this directory to your PythonAnywhere account
3. Place files in your home directory or a subdirectory

### 2. Set Up Virtual Environment
```bash
# In PythonAnywhere console
mkvirtualenv --python=python3.10 cfm56-webapp
pip install -r requirements.txt
```

### 3. Configure Web App
1. Go to the "Web" tab in PythonAnywhere dashboard
2. Click "Add a new web app"
3. Choose "Flask" and Python 3.10
4. Set the source code directory to your uploaded folder
5. Set the WSGI file to: `/home/yourusername/CFM56-7B_WebApp/app.py`

### 4. Update WSGI Configuration
Replace the WSGI file content with:
```python
import sys
path = '/home/yourusername/CFM56-7B_WebApp'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

### 5. Upload Data Files
1. Upload the `data/` folder with your database
2. Upload PDF files to a `static/` folder if needed
3. Update file paths in `app.py` if necessary

### 6. Reload Web App
1. Go to the "Web" tab
2. Click "Reload" to restart your web app
3. Visit your PythonAnywhere URL

## File Structure
```
CFM56-7B_WebApp/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── search.html       # Main search interface
├── static/               # Static files (CSS, JS, images)
└── data/
    └── pdf_linked_database.json  # Search database
```

## Features
- Search across all CFM56-7B document categories
- Direct PDF document access
- Image viewing capabilities
- Category filtering
- Responsive design
- API endpoints for search functionality

## Troubleshooting
- Check PythonAnywhere error logs if the app doesn't load
- Ensure all file paths are correct
- Verify database file is uploaded and accessible
- Check that all dependencies are installed
"""
    
    with open(f"{webapp_dir}/DEPLOYMENT_GUIDE.md", "w") as f:
        f.write(guide_content)
    
    print("✅ Deployment guide created")

def create_zip_package(webapp_dir):
    """Create a zip package for easy upload"""
    import zipfile
    
    zip_path = f"{webapp_dir}/../CFM56-7B_WebApp_Package.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(webapp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, webapp_dir)
                zipf.write(file_path, arc_path)
    
    print(f"✅ Zip package created: {zip_path}")
    return zip_path

def main():
    print("=== CFM56-7B Web Application Package Creator ===")
    
    # Create webapp structure
    webapp_dir = create_webapp_structure()
    
    # Create Flask application
    create_flask_app(webapp_dir)
    
    # Create HTML template
    create_html_template(webapp_dir)
    
    # Copy database
    copy_database(webapp_dir)
    
    # Create requirements file
    create_requirements_file(webapp_dir)
    
    # Create deployment guide
    create_deployment_guide(webapp_dir)
    
    # Create zip package
    zip_path = create_zip_package(webapp_dir)
    
    print(f"\n✅ Web application package created successfully!")
    print(f"📁 Webapp directory: {webapp_dir}")
    print(f"📦 Zip package: {zip_path}")
    print(f"\n🚀 Ready for PythonAnywhere deployment!")
    print(f"📖 See DEPLOYMENT_GUIDE.md for instructions")

if __name__ == "__main__":
    main()
