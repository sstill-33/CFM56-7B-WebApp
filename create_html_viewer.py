#!/usr/bin/env python3
"""
CFM56-7B HTML Document Viewer Generator
Creates a comprehensive HTML-based viewer for all extracted documents
"""

import os
import json
import glob
from pathlib import Path

def create_html_viewer():
    # Set up paths
    base_dir = "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B"
    output_dir = f"{base_dir}_Extracted"
    
    # Create the HTML viewer
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CFM56-7B Aviation Maintenance Documentation</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
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
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
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
        .categories {
            padding: 30px;
        }
        .category-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .category-card {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .category-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .category-header {
            background: #f8f9fa;
            padding: 15px 20px;
            border-bottom: 1px solid #e0e0e0;
            font-weight: 600;
            color: #333;
        }
        .category-content {
            padding: 20px;
        }
        .file-list {
            max-height: 200px;
            overflow-y: auto;
            margin-top: 10px;
        }
        .file-item {
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .file-item:last-child {
            border-bottom: none;
        }
        .file-name {
            color: #333;
            text-decoration: none;
            flex: 1;
        }
        .file-name:hover {
            color: #2a5298;
        }
        .file-size {
            color: #666;
            font-size: 0.9em;
        }
        .search-box {
            margin: 20px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        .search-box input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        .footer {
            background: #333;
            color: white;
            padding: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>CFM56-7B Aviation Maintenance Documentation</h1>
            <p>Comprehensive Technical Documentation System</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number" id="total-pdfs">0</div>
                <div class="stat-label">PDF Documents</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="total-images">0</div>
                <div class="stat-label">Technical Images</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="total-categories">0</div>
                <div class="stat-label">Document Categories</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="total-size">0</div>
                <div class="stat-label">Total Size (MB)</div>
            </div>
        </div>
        
        <div class="categories">
            <h2>Document Categories</h2>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Search documents..." onkeyup="filterDocuments()">
            </div>
            <div class="category-grid" id="categoryGrid">
                <!-- Categories will be populated by JavaScript -->
            </div>
        </div>
        
        <div class="footer">
            <p>CFM56-7B Aviation Maintenance Documentation System | Extracted and Organized for macOS</p>
        </div>
    </div>

    <script>
        // Document data will be populated here
        const documentData = {
            categories: {}
        };

        function loadDocumentData() {
            // This will be populated with actual file data
            documentData.categories = {
                "EIPC": {
                    "name": "Engine Illustrated Parts Catalog",
                    "description": "Detailed parts catalog with illustrations and specifications",
                    "files": []
                },
                "ESM": {
                    "name": "Engine Shop Manual", 
                    "description": "Comprehensive maintenance and repair procedures",
                    "files": []
                },
                "SB": {
                    "name": "Service Bulletins",
                    "description": "Service bulletins and technical updates",
                    "files": []
                },
                "CMM": {
                    "name": "Component Maintenance Manual",
                    "description": "Component-level maintenance procedures",
                    "files": []
                },
                "CPM": {
                    "name": "Component Parts Manual",
                    "description": "Component parts and assembly information",
                    "files": []
                },
                "ITEM": {
                    "name": "Item Documentation",
                    "description": "Individual item specifications and data",
                    "files": []
                },
                "NDTM": {
                    "name": "Non-Destructive Testing Manual",
                    "description": "NDT procedures and techniques",
                    "files": []
                },
                "LLP": {
                    "name": "Life Limited Parts",
                    "description": "Life-limited component documentation",
                    "files": []
                },
                "SOLUTIONS": {
                    "name": "Technical Solutions",
                    "description": "Problem-solving guides and solutions",
                    "files": []
                },
                "SPM": {
                    "name": "Special Procedures Manual",
                    "description": "Special maintenance procedures",
                    "files": []
                },
                "TSP": {
                    "name": "Technical Service Publications",
                    "description": "Technical service information",
                    "files": []
                }
            };
            
            updateDisplay();
        }

        function updateDisplay() {
            const categoryGrid = document.getElementById('categoryGrid');
            categoryGrid.innerHTML = '';
            
            let totalPdfs = 0;
            let totalImages = 0;
            
            for (const [key, category] of Object.entries(documentData.categories)) {
                const categoryCard = document.createElement('div');
                categoryCard.className = 'category-card';
                categoryCard.innerHTML = `
                    <div class="category-header">${category.name}</div>
                    <div class="category-content">
                        <p>${category.description}</p>
                        <div class="file-list">
                            ${category.files.map(file => `
                                <div class="file-item">
                                    <a href="${file.path}" class="file-name" target="_blank">${file.name}</a>
                                    <span class="file-size">${file.size}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `;
                categoryGrid.appendChild(categoryCard);
                
                totalPdfs += category.files.length;
            }
            
            document.getElementById('total-pdfs').textContent = totalPdfs;
            document.getElementById('total-categories').textContent = Object.keys(documentData.categories).length;
        }

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

        // Load data when page loads
        window.onload = loadDocumentData;
    </script>
</body>
</html>
"""
    
    # Write the HTML file
    with open(f"{output_dir}/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"HTML viewer created: {output_dir}/index.html")

if __name__ == "__main__":
    create_html_viewer()
