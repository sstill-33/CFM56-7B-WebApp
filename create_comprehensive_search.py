#!/usr/bin/env python3
"""
Create comprehensive search system for ALL CFM56-7B document categories
Extracts parts, procedures, and references from EIPC, ESM, SB, CMM, CPM, ITEM, NDTM, LLP, SOLUTIONS, SPM, TSP
"""

import os
import json
import glob
import xml.etree.ElementTree as ET
from pathlib import Path

def extract_parts_from_xml(xml_file, category):
    """Extract parts and references from any XML file"""
    parts = []
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Common part number patterns across different document types
        part_patterns = [
            './/pnr',  # Part number
            './/part',  # Part element
            './/item',  # Item element
            './/ref',   # Reference
            './/partnbr',  # Part number
            './/partnumber',  # Part number
        ]
        
        for pattern in part_patterns:
            for element in root.findall(pattern):
                part_text = element.text
                if part_text and len(part_text.strip()) > 3:  # Filter out very short strings
                    # Get description from nearby elements
                    description = ""
                    for desc_pattern in ['.//nom', './/title', './/name', './/description']:
                        desc_elem = element.find(desc_pattern)
                        if desc_elem is not None and desc_elem.text:
                            description = desc_elem.text.strip()
                            break
                    
                    # Get chapter/section info
                    chapter = ""
                    section = ""
                    figure = ""
                    
                    # Look for chapter/section in current element attributes
                    if 'chapnbr' in element.attrib:
                        chapter = element.attrib['chapnbr']
                    if 'sectnbr' in element.attrib:
                        section = element.attrib['sectnbr']
                    if 'fignbr' in element.attrib:
                        figure = element.attrib['fignbr']
                    
                    # Look for image references
                    image_file = ""
                    for img_pattern in ['.//sheet', './/graphic', './/image']:
                        img_elem = element.find(img_pattern)
                        if img_elem is not None and 'uncfile' in img_elem.attrib:
                            image_file = img_elem.attrib['uncfile']
                            break
                    
                    parts.append({
                        'part_number': part_text.strip(),
                        'description': description,
                        'chapter': chapter,
                        'section': section,
                        'figure': figure,
                        'image_file': image_file,
                        'source_file': xml_file,
                        'category': category
                    })
        
        # Also extract any text content that might contain part numbers
        for elem in root.iter():
            if elem.text and len(elem.text.strip()) > 5:
                text = elem.text.strip()
                # Look for patterns that might be part numbers
                import re
                part_matches = re.findall(r'\b[A-Z0-9]{6,15}\b', text)
                for match in part_matches:
                    if len(match) >= 6:  # Reasonable part number length
                        parts.append({
                            'part_number': match,
                            'description': text[:100] + "..." if len(text) > 100 else text,
                            'chapter': "",
                            'section': "",
                            'figure': "",
                            'image_file': "",
                            'source_file': xml_file,
                            'category': category
                        })
    
    except Exception as e:
        print(f"Error parsing {xml_file}: {e}")
    
    return parts

def extract_service_bulletins():
    """Extract service bulletins from CSV and XML files"""
    base_dir = "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B"
    service_bulletins = []
    
    # Extract from CSV
    csv_file = f"{base_dir}/datas/sbindex.csv"
    if os.path.exists(csv_file):
        try:
            with open(csv_file, 'r', encoding='latin-1') as f:  # Try latin-1 encoding
                for line in f:
                    parts = line.strip().split(';')
                    if len(parts) >= 7:
                        service_bulletins.append({
                            'title': parts[6],
                            'date': parts[3],
                            'category': 'SB',
                            'source': 'CSV'
                        })
        except UnicodeDecodeError:
            try:
                with open(csv_file, 'r', encoding='cp1252') as f:  # Try cp1252 encoding
                    for line in f:
                        parts = line.strip().split(';')
                        if len(parts) >= 7:
                            service_bulletins.append({
                                'title': parts[6],
                                'date': parts[3],
                                'category': 'SB',
                                'source': 'CSV'
                            })
            except UnicodeDecodeError:
                print(f"Warning: Could not decode CSV file {csv_file}")
    
    # Extract from XML files
    xml_files = glob.glob(f"{base_dir}/datas/data/SB/7B/*.xml")
    for xml_file in xml_files:
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # Extract title and content
            title = ""
            for title_elem in root.findall('.//title'):
                if title_elem.text:
                    title = title_elem.text.strip()
                    break
            
            # Extract any part numbers mentioned
            parts = extract_parts_from_xml(xml_file, 'SB')
            
            if title:
                service_bulletins.append({
                    'title': title,
                    'parts': parts,
                    'category': 'SB',
                    'source': 'XML',
                    'source_file': xml_file
                })
        
        except Exception as e:
            print(f"Error parsing SB XML {xml_file}: {e}")
    
    return service_bulletins

def build_comprehensive_database():
    """Build comprehensive database from all categories"""
    base_dir = "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B"
    output_dir = f"{base_dir}_Extracted"
    
    print("=== CFM56-7B Comprehensive Search Database ===")
    print("Building database from ALL document categories...")
    
    # All categories to process
    categories = {
        'EIPC': 'Engine Illustrated Parts Catalog',
        'ESM': 'Engine Shop Manual',
        'SB': 'Service Bulletins',
        'CMM': 'Component Maintenance Manual',
        'CPM': 'Component Parts Manual',
        'ITEM': 'Item Documentation',
        'NDTM': 'Non-Destructive Testing Manual',
        'LLP': 'Life Limited Parts',
        'SOLUTIONS': 'Technical Solutions',
        'SPM': 'Special Procedures Manual',
        'TSP': 'Technical Service Publications'
    }
    
    all_parts = []
    all_documents = []
    all_service_bulletins = []
    
    # Process each category
    for cat_key, cat_name in categories.items():
        print(f"\nProcessing {cat_name} ({cat_key})...")
        
        # Find XML files in this category
        xml_files = glob.glob(f"{base_dir}/datas/data/{cat_key}/7B/*.xml")
        print(f"  Found {len(xml_files)} XML files")
        
        # Extract parts from XML files
        for xml_file in xml_files:
            parts = extract_parts_from_xml(xml_file, cat_key)
            all_parts.extend(parts)
        
        # Find PDF files in this category
        pdf_files = glob.glob(f"{base_dir}/datas/data/{cat_key}/7B/*.pdf")
        print(f"  Found {len(pdf_files)} PDF files")
        
        for pdf_file in pdf_files:
            all_documents.append({
                'name': os.path.basename(pdf_file),
                'path': pdf_file,
                'category': cat_key,
                'category_name': cat_name,
                'size_mb': round(os.path.getsize(pdf_file) / (1024 * 1024), 2)
            })
    
    # Extract service bulletins
    print(f"\nProcessing Service Bulletins...")
    all_service_bulletins = extract_service_bulletins()
    print(f"  Found {len(all_service_bulletins)} service bulletins")
    
    # Create comprehensive database
    database = {
        'parts': all_parts,
        'documents': all_documents,
        'service_bulletins': all_service_bulletins,
        'categories': categories,
        'stats': {
            'total_parts': len(all_parts),
            'total_documents': len(all_documents),
            'total_service_bulletins': len(all_service_bulletins),
            'total_categories': len(categories)
        }
    }
    
    # Save database
    os.makedirs(output_dir, exist_ok=True)
    db_file = f"{output_dir}/comprehensive_database.json"
    with open(db_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Comprehensive database created!")
    print(f"   Database file: {db_file}")
    print(f"   Total parts: {len(all_parts)}")
    print(f"   Total documents: {len(all_documents)}")
    print(f"   Total service bulletins: {len(all_service_bulletins)}")
    
    return database

def create_comprehensive_search_viewer(database):
    """Create comprehensive search viewer for all categories"""
    output_dir = "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B_Extracted"
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CFM56-7B Comprehensive Search System</title>
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
        .filter-section {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }}
        .filter-button {{
            padding: 8px 16px;
            background: #f8f9fa;
            border: 1px solid #ddd;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .filter-button.active {{
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
            font-size: 1.3em;
            font-weight: 600;
            color: #2a5298;
            margin-bottom: 10px;
        }}
        .result-description {{
            color: #333;
            margin-bottom: 10px;
            font-size: 1.1em;
        }}
        .result-details {{
            color: #666;
            margin-bottom: 15px;
            font-size: 0.9em;
        }}
        .result-actions {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
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
        .category-badge {{
            display: inline-block;
            padding: 4px 8px;
            background: #e3f2fd;
            color: #1976d2;
            border-radius: 4px;
            font-size: 0.8em;
            margin-right: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>CFM56-7B Comprehensive Search System</h1>
            <p>Search across ALL document categories: EIPC, ESM, SB, CMM, CPM, ITEM, NDTM, LLP, SOLUTIONS, SPM, TSP</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{database['stats']['total_parts']}</div>
                <div class="stat-label">Parts & References</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{database['stats']['total_documents']}</div>
                <div class="stat-label">PDF Documents</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{database['stats']['total_service_bulletins']}</div>
                <div class="stat-label">Service Bulletins</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{database['stats']['total_categories']}</div>
                <div class="stat-label">Categories</div>
            </div>
        </div>
        
        <div class="search-section">
            <div class="search-container">
                <input type="text" id="searchInput" class="search-input" placeholder="Search parts, procedures, service bulletins, or any reference..." onkeyup="handleSearch()">
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
                    <h3>Search across all CFM56-7B documentation</h3>
                    <p>Enter a search term to find parts, procedures, service bulletins, or any reference across all categories</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        const database = {json.dumps(database, indent=2)};
        let currentFilter = 'all';
        
        function handleSearch() {{
            const query = document.getElementById('searchInput').value.trim();
            if (query.length >= 2) {{
                performSearch();
            }} else {{
                showNoResults();
            }}
        }}
        
        function filterByCategory(category) {{
            currentFilter = category;
            
            // Update filter buttons
            document.querySelectorAll('.filter-button').forEach(btn => {{
                btn.classList.remove('active');
            }});
            event.target.classList.add('active');
            
            // Re-run search if there's a query
            const query = document.getElementById('searchInput').value.trim();
            if (query.length >= 2) {{
                performSearch();
            }}
        }}
        
        function performSearch() {{
            const query = document.getElementById('searchInput').value.trim().toLowerCase();
            if (query.length < 2) {{
                showNoResults();
                return;
            }}
            
            let results = [];
            
            // Search parts
            database.parts.forEach(part => {{
                if (currentFilter !== 'all' && part.category !== currentFilter) return;
                
                if (part.part_number && part.part_number.toLowerCase().includes(query)) {{
                    results.push({{
                        type: 'part',
                        title: part.part_number,
                        description: part.description || 'No description available',
                        details: `Category: ${{part.category}} | Chapter: ${{part.chapter}}-${{part.section}}-${{part.unit}} | Figure: ${{part.figure}}`,
                        category: part.category,
                        actions: getActionsForPart(part)
                    }});
                }} else if (part.description && part.description.toLowerCase().includes(query)) {{
                    results.push({{
                        type: 'part',
                        title: part.part_number || 'Unknown Part',
                        description: part.description,
                        details: `Category: ${{part.category}} | Chapter: ${{part.chapter}}-${{part.section}}-${{part.unit}} | Figure: ${{part.figure}}`,
                        category: part.category,
                        actions: getActionsForPart(part)
                    }});
                }}
            }});
            
            // Search service bulletins
            database.service_bulletins.forEach(sb => {{
                if (currentFilter !== 'all' && sb.category !== currentFilter) return;
                
                if (sb.title && sb.title.toLowerCase().includes(query)) {{
                    results.push({{
                        type: 'service_bulletin',
                        title: sb.title,
                        description: `Service Bulletin - ${{sb.date || 'No date'}}`,
                        details: `Category: ${{sb.category}} | Source: ${{sb.source}}`,
                        category: sb.category,
                        actions: getActionsForServiceBulletin(sb)
                    }});
                }}
            }});
            
            // Search documents
            database.documents.forEach(doc => {{
                if (currentFilter !== 'all' && doc.category !== currentFilter) return;
                
                if (doc.name && doc.name.toLowerCase().includes(query)) {{
                    results.push({{
                        type: 'document',
                        title: doc.name,
                        description: `${{doc.category_name}} - ${{doc.size_mb}} MB`,
                        details: `Category: ${{doc.category}} | Size: ${{doc.size_mb}} MB`,
                        category: doc.category,
                        actions: getActionsForDocument(doc)
                    }});
                }}
            }});
            
            displayResults(results);
        }}
        
        function getActionsForPart(part) {{
            const actions = [];
            
            if (part.source_file) {{
                actions.push({{text: 'View Source XML', url: `file://${{part.source_file}}`}});
            }}
            
            if (part.image_file) {{
                actions.push({{text: 'View Image', url: `file://${{part.image_file}}`}});
            }}
            
            return actions;
        }}
        
        function getActionsForServiceBulletin(sb) {{
            const actions = [];
            
            if (sb.source_file) {{
                actions.push({{text: 'View Source XML', url: `file://${{sb.source_file}}`}});
            }}
            
            return actions;
        }}
        
        function getActionsForDocument(doc) {{
            const actions = [];
            
            if (doc.path) {{
                actions.push({{text: 'View PDF', url: `file://${{doc.path}}`}});
            }}
            
            return actions;
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
                        <div class="result-title">
                            ${{result.title}}
                            <span class="category-badge">${{result.category}}</span>
                        </div>
                        <div class="result-description">${{result.description}}</div>
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
                    <p>Try searching for part numbers, keywords, or document titles across all categories</p>
                </div>
            `;
        }}
    </script>
</body>
</html>
"""
    
    # Write the HTML file
    with open(f"{output_dir}/comprehensive_search.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Comprehensive search viewer created: {output_dir}/comprehensive_search.html")
    return f"{output_dir}/comprehensive_search.html"

def main():
    print("=== CFM56-7B Comprehensive Search System ===")
    
    # Build comprehensive database
    database = build_comprehensive_database()
    
    # Create comprehensive search viewer
    html_file = create_comprehensive_search_viewer(database)
    
    print(f"\n✅ Comprehensive search system created!")
    print(f"   Search system: {html_file}")
    print(f"\nFeatures:")
    print(f"   - Search across ALL {database['stats']['total_categories']} categories")
    print(f"   - {database['stats']['total_parts']} parts and references")
    print(f"   - {database['stats']['total_documents']} PDF documents")
    print(f"   - {database['stats']['total_service_bulletins']} service bulletins")
    print(f"   - Filter by category")
    print(f"   - Direct links to source files")

if __name__ == "__main__":
    main()
