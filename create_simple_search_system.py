#!/usr/bin/env python3
"""
Simple but robust CFM56-7B Search System Generator
Creates a search system that works with the available data
"""

import os
import json
import xml.etree.ElementTree as ET
import csv
import glob
from pathlib import Path
import re

def extract_parts_from_xml_simple(xml_file):
    """Extract part numbers using a simpler approach"""
    parts = []
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Find all part numbers in the XML
        for pnr in root.findall('.//pnr'):
            if pnr.text:
                part_info = {
                    'part_number': pnr.text,
                    'source_file': xml_file
                }
                
                # Try to get description from parent nom element
                nom_elem = pnr.getparent()
                if nom_elem is not None and nom_elem.tag == 'nom':
                    kwd = nom_elem.find('kwd')
                    adt = nom_elem.find('adt')
                    if kwd is not None and adt is not None:
                        part_info['description'] = f"{kwd.text} {adt.text}".strip()
                    elif kwd is not None:
                        part_info['description'] = kwd.text
                
                # Try to get figure reference
                item_elem = pnr.getparent()
                if item_elem is not None:
                    part_info['chapter'] = item_elem.get('chapnbr', '')
                    part_info['section'] = item_elem.get('sectnbr', '')
                    part_info['unit'] = item_elem.get('unitnbr', '')
                    part_info['figure'] = item_elem.get('fignbr', '')
                    part_info['item'] = item_elem.get('itemnbr', '')
                
                # Try to find image file in the same document
                for sheet in root.findall('.//sheet'):
                    uncfile = sheet.get('uncfile', '')
                    if uncfile:
                        part_info['image_file'] = uncfile
                        break
                
                parts.append(part_info)
    
    except Exception as e:
        print(f"Error parsing {xml_file}: {e}")
    
    return parts

def extract_service_bulletins_simple(csv_file):
    """Extract service bulletins with proper encoding"""
    service_bulletins = []
    try:
        with open(csv_file, 'r', encoding='latin-1') as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                if len(row) >= 7:
                    sb_info = {
                        'model': row[0],
                        'chapter': row[1],
                        'section': row[2],
                        'date': row[3],
                        'revision': row[4],
                        'type': row[5],
                        'title': row[6],
                        'effective_date': row[7] if len(row) > 7 else row[3]
                    }
                    service_bulletins.append(sb_info)
    except Exception as e:
        print(f"Error parsing {csv_file}: {e}")
    
    return service_bulletins

def build_simple_search_database():
    """Build a simple but comprehensive search database"""
    base_dir = "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B"
    output_dir = f"{base_dir}_Extracted"
    
    print("Building simple search database...")
    
    # Initialize database
    search_db = {
        'parts': [],
        'service_bulletins': [],
        'documents': [],
        'images': [],
        'search_index': {}
    }
    
    # Extract parts from a few sample EIPC XML files
    print("Extracting part numbers from sample EIPC files...")
    eipc_xml_files = glob.glob(f"{base_dir}/datas/data/EIPC/7B/*.xml")[:50]  # Limit to first 50 files
    for xml_file in eipc_xml_files:
        parts = extract_parts_from_xml_simple(xml_file)
        for part in parts:
            part['category'] = 'EIPC'
            search_db['parts'].append(part)
    
    # Extract service bulletins
    print("Extracting service bulletins...")
    sb_csv = f"{base_dir}/datas/sbindex.csv"
    if os.path.exists(sb_csv):
        search_db['service_bulletins'] = extract_service_bulletins_simple(sb_csv)
    
    # Build document index
    print("Building document index...")
    categories = ['EIPC', 'ESM', 'SB', 'CMM', 'CPM', 'ITEM', 'NDTM', 'LLP', 'SOLUTIONS', 'SPM', 'TSP']
    for category in categories:
        pdf_files = glob.glob(f"{base_dir}/datas/data/{category}/7B/*.pdf")
        for pdf_file in pdf_files:
            doc_info = {
                'name': os.path.basename(pdf_file),
                'path': pdf_file,
                'category': category,
                'size_mb': round(os.path.getsize(pdf_file) / (1024 * 1024), 2)
            }
            search_db['documents'].append(doc_info)
    
    # Build image index
    print("Building image index...")
    image_files = glob.glob(f"{base_dir}/datas/art/**/*.tif", recursive=True)
    for img_file in image_files:
        img_info = {
            'name': os.path.basename(img_file),
            'path': img_file,
            'category': 'ART'
        }
        search_db['images'].append(img_info)
    
    # Build search index
    print("Building search index...")
    search_terms = set()
    
    # Add part numbers
    for part in search_db['parts']:
        if 'part_number' in part:
            search_terms.add(part['part_number'])
        if 'description' in part:
            words = part['description'].split()
            search_terms.update(words)
    
    # Add service bulletin titles
    for sb in search_db['service_bulletins']:
        words = sb['title'].split()
        search_terms.update(words)
    
    # Add document names
    for doc in search_db['documents']:
        words = doc['name'].replace('.pdf', '').replace('_', ' ').split()
        search_terms.update(words)
    
    search_db['search_index'] = list(search_terms)
    
    # Save database
    db_file = f"{output_dir}/search_database.json"
    with open(db_file, 'w', encoding='utf-8') as f:
        json.dump(search_db, f, indent=2, ensure_ascii=False)
    
    print(f"Search database created: {db_file}")
    print(f"Total parts: {len(search_db['parts'])}")
    print(f"Total service bulletins: {len(search_db['service_bulletins'])}")
    print(f"Total documents: {len(search_db['documents'])}")
    print(f"Total images: {len(search_db['images'])}")
    print(f"Total search terms: {len(search_db['search_index'])}")
    
    return search_db

def create_simple_html_viewer(search_db):
    """Create a simple but effective HTML viewer"""
    output_dir = "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B_Extracted"
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CFM56-7B Search System</title>
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
        .search-section {{
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
        }}
        .search-container {{
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 15px;
            margin-bottom: 20px;
        }}
        .search-input {{
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }}
        .search-input:focus {{
            outline: none;
            border-color: #2a5298;
        }}
        .search-button {{
            padding: 15px 30px;
            background: #2a5298;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }}
        .search-button:hover {{
            background: #1e3c72;
        }}
        .search-tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }}
        .tab-button {{
            padding: 10px 20px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .tab-button.active {{
            background: #2a5298;
            color: white;
        }}
        .results-section {{
            padding: 30px;
        }}
        .result-item {{
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            transition: box-shadow 0.3s;
        }}
        .result-item:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        .result-title {{
            font-size: 1.2em;
            font-weight: 600;
            color: #333;
            margin-bottom: 10px;
        }}
        .result-details {{
            color: #666;
            margin-bottom: 10px;
        }}
        .result-actions {{
            display: flex;
            gap: 10px;
        }}
        .action-button {{
            padding: 8px 16px;
            background: #f8f9fa;
            border: 1px solid #ddd;
            border-radius: 4px;
            text-decoration: none;
            color: #333;
            font-size: 0.9em;
            transition: all 0.3s;
        }}
        .action-button:hover {{
            background: #2a5298;
            color: white;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 20px;
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
        .no-results {{
            text-align: center;
            padding: 40px;
            color: #666;
        }}
        .part-highlight {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>CFM56-7B Search System</h1>
            <p>Search by part numbers, keywords, or document titles</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(search_db['parts'])}</div>
                <div class="stat-label">Part Numbers</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(search_db['service_bulletins'])}</div>
                <div class="stat-label">Service Bulletins</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(search_db['documents'])}</div>
                <div class="stat-label">Documents</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(search_db['images'])}</div>
                <div class="stat-label">Images</div>
            </div>
        </div>
        
        <div class="search-section">
            <div class="search-container">
                <input type="text" id="searchInput" class="search-input" placeholder="Enter part number, keyword, or document title..." onkeyup="handleSearch()">
                <button onclick="performSearch()" class="search-button">Search</button>
            </div>
            <div class="search-tabs">
                <button class="tab-button active" onclick="setActiveTab('all')">All Results</button>
                <button class="tab-button" onclick="setActiveTab('parts')">Parts</button>
                <button class="tab-button" onclick="setActiveTab('documents')">Documents</button>
                <button class="tab-button" onclick="setActiveTab('service_bulletins')">Service Bulletins</button>
            </div>
        </div>
        
        <div class="results-section">
            <div id="searchResults">
                <div class="no-results">
                    <h3>Enter a search term to find parts, documents, or service bulletins</h3>
                    <p>Try searching for part numbers like "9324M60G01" or keywords like "engine" or "fan"</p>
                    <div class="part-highlight">
                        <strong>Sample Part Numbers:</strong><br>
                        9324M60G01, 9324M60G02, 9324M60G03, 9324M60G04, 9324M60G05
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const searchDatabase = {json.dumps(search_db, indent=2)};
        let currentTab = 'all';
        
        function setActiveTab(tab) {{
            currentTab = tab;
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            performSearch();
        }}
        
        function handleSearch() {{
            const query = document.getElementById('searchInput').value.trim();
            if (query.length >= 2) {{
                performSearch();
            }} else {{
                showNoResults();
            }}
        }}
        
        function performSearch() {{
            const query = document.getElementById('searchInput').value.trim().toLowerCase();
            if (query.length < 2) {{
                showNoResults();
                return;
            }}
            
            let results = [];
            
            if (currentTab === 'all' || currentTab === 'parts') {{
                // Search parts
                searchDatabase.parts.forEach(part => {{
                    if (part.part_number && part.part_number.toLowerCase().includes(query)) {{
                        results.push({{
                            type: 'part',
                            title: part.part_number,
                            description: part.description || 'No description available',
                            details: `Chapter: ${{part.chapter}}-${{part.section}}-${{part.unit}} | Figure: ${{part.figure}}`,
                            actions: [
                                {{text: 'View Document', url: `file://${{part.source_file}}`}},
                                {{text: 'View Image', url: `file://${{part.image_file}}`}}
                            ]
                        }});
                    }} else if (part.description && part.description.toLowerCase().includes(query)) {{
                        results.push({{
                            type: 'part',
                            title: part.part_number || 'Unknown Part',
                            description: part.description,
                            details: `Chapter: ${{part.chapter}}-${{part.section}}-${{part.unit}} | Figure: ${{part.figure}}`,
                            actions: [
                                {{text: 'View Document', url: `file://${{part.source_file}}`}},
                                {{text: 'View Image', url: `file://${{part.image_file}}`}}
                            ]
                        }});
                    }}
                }});
            }}
            
            if (currentTab === 'all' || currentTab === 'documents') {{
                // Search documents
                searchDatabase.documents.forEach(doc => {{
                    if (doc.name.toLowerCase().includes(query)) {{
                        results.push({{
                            type: 'document',
                            title: doc.name,
                            description: `${{doc.category}} Document`,
                            details: `Size: ${{doc.size_mb}} MB | Category: ${{doc.category}}`,
                            actions: [
                                {{text: 'Open PDF', url: `file://${{doc.path}}`}}
                            ]
                        }});
                    }}
                }});
            }}
            
            if (currentTab === 'all' || currentTab === 'service_bulletins') {{
                // Search service bulletins
                searchDatabase.service_bulletins.forEach(sb => {{
                    if (sb.title.toLowerCase().includes(query)) {{
                        results.push({{
                            type: 'service_bulletin',
                            title: `SB ${{sb.chapter}}-${{sb.section}}`,
                            description: sb.title,
                            details: `Date: ${{sb.date}} | Revision: ${{sb.revision}} | Type: ${{sb.type}}`,
                            actions: [
                                {{text: 'View Details', url: '#'}}
                            ]
                        }});
                    }}
                }});
            }}
            
            displayResults(results);
        }}
        
        function displayResults(results) {{
            const resultsContainer = document.getElementById('searchResults');
            
            if (results.length === 0) {{
                showNoResults();
                return;
            }}
            
            let html = '';
            results.forEach(result => {{
                html += `
                    <div class="result-item">
                        <div class="result-title">${{result.title}}</div>
                        <div class="result-details">${{result.description}}</div>
                        <div class="result-details">${{result.details}}</div>
                        <div class="result-actions">
                            ${{result.actions.map(action => 
                                `<a href="${{action.url}}" class="action-button" target="_blank">${{action.text}}</a>`
                            ).join('')}}
                        </div>
                    </div>
                `;
            }});
            
            resultsContainer.innerHTML = html;
        }}
        
        function showNoResults() {{
            const resultsContainer = document.getElementById('searchResults');
            resultsContainer.innerHTML = `
                <div class="no-results">
                    <h3>No results found</h3>
                    <p>Try searching for part numbers, keywords, or document titles</p>
                </div>
            `;
        }}
    </script>
</body>
</html>
"""
    
    # Write the HTML file
    with open(f"{output_dir}/search_system.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Search system created: {output_dir}/search_system.html")
    return f"{output_dir}/search_system.html"

def main():
    print("=== CFM56-7B Simple Search System Generator ===")
    
    # Build search database
    search_db = build_simple_search_database()
    
    # Create HTML viewer
    html_file = create_simple_html_viewer(search_db)
    
    print(f"\n✅ Search system created!")
    print(f"   Main viewer: /Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B_Extracted/index.html")
    print(f"   Search system: {html_file}")
    print(f"\nFeatures:")
    print(f"   - Search by part numbers")
    print(f"   - Search by keywords")
    print(f"   - Search by document titles")
    print(f"   - Direct links to PDFs and images")
    print(f"   - Part number to image linking")

if __name__ == "__main__":
    main()
