#!/usr/bin/env python3
"""
Complete CFM56-7B HTML Viewer Generator
Scans the actual files and creates a comprehensive HTML viewer
"""

import os
import json
import glob
from pathlib import Path
import subprocess

def get_file_size_mb(file_path):
    """Get file size in MB"""
    try:
        size_bytes = os.path.getsize(file_path)
        return round(size_bytes / (1024 * 1024), 2)
    except:
        return 0

def scan_documents():
    """Scan all documents and create organized structure"""
    base_dir = "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B"
    output_dir = f"{base_dir}_Extracted"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Document categories and their paths
    categories = {
        "EIPC": {
            "name": "Engine Illustrated Parts Catalog",
            "description": "Detailed parts catalog with illustrations and specifications",
            "path": f"{base_dir}/datas/data/EIPC/7B",
            "files": []
        },
        "ESM": {
            "name": "Engine Shop Manual", 
            "description": "Comprehensive maintenance and repair procedures",
            "path": f"{base_dir}/datas/data/ESM/7B",
            "files": []
        },
        "SB": {
            "name": "Service Bulletins",
            "description": "Service bulletins and technical updates",
            "path": f"{base_dir}/datas/data/SB/7B",
            "files": []
        },
        "CMM": {
            "name": "Component Maintenance Manual",
            "description": "Component-level maintenance procedures",
            "path": f"{base_dir}/datas/data/CMM/7B",
            "files": []
        },
        "CPM": {
            "name": "Component Parts Manual",
            "description": "Component parts and assembly information",
            "path": f"{base_dir}/datas/data/CPM/7B",
            "files": []
        },
        "ITEM": {
            "name": "Item Documentation",
            "description": "Individual item specifications and data",
            "path": f"{base_dir}/datas/data/ITEM/7B",
            "files": []
        },
        "NDTM": {
            "name": "Non-Destructive Testing Manual",
            "description": "NDT procedures and techniques",
            "path": f"{base_dir}/datas/data/NDTM/7B",
            "files": []
        },
        "LLP": {
            "name": "Life Limited Parts",
            "description": "Life-limited component documentation",
            "path": f"{base_dir}/datas/data/LLP/7B",
            "files": []
        },
        "SOLUTIONS": {
            "name": "Technical Solutions",
            "description": "Problem-solving guides and solutions",
            "path": f"{base_dir}/datas/data/SOLUTIONS/7B",
            "files": []
        },
        "SPM": {
            "name": "Special Procedures Manual",
            "description": "Special maintenance procedures",
            "path": f"{base_dir}/datas/data/SPM/7B",
            "files": []
        },
        "TSP": {
            "name": "Technical Service Publications",
            "description": "Technical service information",
            "path": f"{base_dir}/datas/data/TSP/7B",
            "files": []
        }
    }
    
    total_files = 0
    total_size = 0
    
    print("Scanning documents...")
    
    # Scan each category
    for cat_key, cat_data in categories.items():
        print(f"Scanning {cat_data['name']}...")
        
        if os.path.exists(cat_data['path']):
            # Find all PDF files
            pdf_files = glob.glob(f"{cat_data['path']}/**/*.pdf", recursive=True)
            
            for pdf_file in pdf_files:
                file_name = os.path.basename(pdf_file)
                file_size = get_file_size_mb(pdf_file)
                
                cat_data['files'].append({
                    'name': file_name,
                    'path': pdf_file,
                    'size': f"{file_size} MB",
                    'size_mb': file_size
                })
                
                total_files += 1
                total_size += file_size
    
    return categories, total_files, total_size

def create_html_viewer(categories, total_files, total_size):
    """Create the HTML viewer"""
    output_dir = "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B_Extracted"
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CFM56-7B Aviation Maintenance Documentation</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #2a5298;
        }}
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        .categories {{
            padding: 30px;
        }}
        .search-box {{
            margin: 20px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        .search-box input {{
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }}
        .category-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .category-card {{
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .category-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .category-header {{
            background: #f8f9fa;
            padding: 15px 20px;
            border-bottom: 1px solid #e0e0e0;
            font-weight: 600;
            color: #333;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .file-count {{
            background: #2a5298;
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
        }}
        .category-content {{
            padding: 20px;
        }}
        .file-list {{
            max-height: 300px;
            overflow-y: auto;
            margin-top: 10px;
        }}
        .file-item {{
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .file-item:last-child {{
            border-bottom: none;
        }}
        .file-name {{
            color: #333;
            text-decoration: none;
            flex: 1;
            font-size: 0.9em;
        }}
        .file-name:hover {{
            color: #2a5298;
        }}
        .file-size {{
            color: #666;
            font-size: 0.8em;
        }}
        .footer {{
            background: #333;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .instructions {{
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>CFM56-7B Aviation Maintenance Documentation</h1>
            <p>Comprehensive Technical Documentation System - {total_files} Documents</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{total_files}</div>
                <div class="stat-label">PDF Documents</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(categories)}</div>
                <div class="stat-label">Document Categories</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_size:.0f}</div>
                <div class="stat-label">Total Size (MB)</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">CFM56-7B</div>
                <div class="stat-label">Engine Model</div>
            </div>
        </div>
        
        <div class="categories">
            <h2>Document Categories</h2>
            <div class="instructions">
                <strong>How to use:</strong> Click on any PDF document to open it directly in your browser or download it. 
                Use the search box to quickly find specific documents. All documents are organized by category for easy navigation.
            </div>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Search documents by name..." onkeyup="filterDocuments()">
            </div>
            <div class="category-grid" id="categoryGrid">
"""
    
    # Add category cards
    for cat_key, cat_data in categories.items():
        if cat_data['files']:  # Only show categories with files
            html_content += f"""
                <div class="category-card">
                    <div class="category-header">
                        <span>{cat_data['name']}</span>
                        <span class="file-count">{len(cat_data['files'])} files</span>
                    </div>
                    <div class="category-content">
                        <p>{cat_data['description']}</p>
                        <div class="file-list">
"""
            # Add files (limit to first 20 for performance)
            for file_info in cat_data['files'][:20]:
                html_content += f"""
                            <div class="file-item">
                                <a href="file://{file_info['path']}" class="file-name" target="_blank">{file_info['name']}</a>
                                <span class="file-size">{file_info['size']}</span>
                            </div>
"""
            if len(cat_data['files']) > 20:
                html_content += f"""
                            <div class="file-item">
                                <span class="file-name" style="color: #666;">... and {len(cat_data['files']) - 20} more files</span>
                            </div>
"""
            html_content += """
                        </div>
                    </div>
                </div>
"""
    
    html_content += """
            </div>
        </div>
        
        <div class="footer">
            <p>CFM56-7B Aviation Maintenance Documentation System | Extracted and Organized for macOS</p>
            <p>All documents are accessible directly from this interface</p>
        </div>
    </div>

    <script>
        function filterDocuments() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const categoryCards = document.querySelectorAll('.category-card');
            
            categoryCards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>
"""
    
    # Write the HTML file
    with open(f"{output_dir}/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"HTML viewer created: {output_dir}/index.html")
    return f"{output_dir}/index.html"

def main():
    print("=== CFM56-7B Document Viewer Generator ===")
    print("Scanning and organizing documents...")
    
    # Scan documents
    categories, total_files, total_size = scan_documents()
    
    print(f"Found {total_files} documents totaling {total_size:.1f} MB")
    
    # Create HTML viewer
    html_file = create_html_viewer(categories, total_files, total_size)
    
    print(f"\n✅ Complete! Open this file in your browser:")
    print(f"   {html_file}")
    print(f"\nYou can also open it by double-clicking the file in Finder.")

if __name__ == "__main__":
    main()
