#!/usr/bin/env python3
"""
Create search system with proper PDF document linking
Maps XML parts to their corresponding PDF documents
"""

import os
import json
import glob
import xml.etree.ElementTree as ET
from pathlib import Path

def find_pdf_for_xml(xml_file, category):
    """Find the corresponding PDF file for an XML file"""
    base_dir = "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B"
    
    # Get the base name without extension
    xml_basename = os.path.splitext(os.path.basename(xml_file))[0]
    
    # Look for PDF with similar name in the same category
    pdf_patterns = [
        f"{base_dir}/datas/data/{category}/7B/{xml_basename}.pdf",
        f"{base_dir}/datas/data/{category}/7B/{xml_basename}*.pdf",
    ]
    
    for pattern in pdf_patterns:
        pdf_files = glob.glob(pattern)
        if pdf_files:
            return pdf_files[0]
    
    # If no exact match, find any PDF in the same category
    pdf_files = glob.glob(f"{base_dir}/datas/data/{category}/7B/*.pdf")
    if pdf_files:
        return pdf_files[0]
    
    return None

def find_image_for_xml(xml_file, category):
    """Find images related to an XML file"""
    base_dir = "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B"
    
    # Look for images in the art directory
    image_patterns = [
        f"{base_dir}/datas/art/{category}/7B/*.tif",
        f"{base_dir}/datas/art/EIPC/7B/*.tif",  # EIPC has most images
        f"{base_dir}/datas/art/**/*.tif",  # Any image
    ]
    
    for pattern in image_patterns:
        image_files = glob.glob(pattern)
        if image_files:
            return image_files[0]
    
    return None

def extract_parts_with_pdf_links(xml_file, category):
    """Extract parts and link them to PDF documents"""
    parts = []
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Find the corresponding PDF
        pdf_file = find_pdf_for_xml(xml_file, category)
        image_file = find_image_for_xml(xml_file, category)
        
        # Get document title from XML
        document_title = ""
        for title_pattern in ['.//title', './/name', './/docnbr']:
            title_elem = root.find(title_pattern)
            if title_elem is not None and title_elem.text:
                document_title = title_elem.text.strip()
                break
        
        # If no title found, use filename
        if not document_title:
            document_title = os.path.splitext(os.path.basename(xml_file))[0]
        
        # Extract part numbers
        part_patterns = [
            './/pnr',  # Part number
            './/part',  # Part element
            './/item',  # Item element
            './/ref',   # Reference
        ]
        
        for pattern in part_patterns:
            for element in root.findall(pattern):
                part_text = element.text
                if part_text and len(part_text.strip()) > 3:
                    # Get description
                    description = ""
                    for desc_pattern in ['.//nom', './/title', './/name', './/description']:
                        desc_elem = element.find(desc_pattern)
                        if desc_elem is not None and desc_elem.text:
                            description = desc_elem.text.strip()
                            break
                    
                    # Get chapter/section info
                    chapter = element.attrib.get('chapnbr', '')
                    section = element.attrib.get('sectnbr', '')
                    figure = element.attrib.get('fignbr', '')
                    
                    # Look for image references
                    image_ref = ""
                    for img_pattern in ['.//sheet', './/graphic', './/image']:
                        img_elem = element.find(img_pattern)
                        if img_elem is not None and 'uncfile' in img_elem.attrib:
                            image_ref = img_elem.attrib['uncfile']
                            break
                    
                    parts.append({
                        'document_title': document_title,
                        'part_number': part_text.strip(),
                        'description': description,
                        'chapter': chapter,
                        'section': section,
                        'figure': figure,
                        'image_file': image_ref or image_file,
                        'pdf_file': pdf_file,
                        'source_file': xml_file,
                        'category': category
                    })
        
        # Also extract any text content that might contain part numbers
        for elem in root.iter():
            if elem.text and len(elem.text.strip()) > 5:
                text = elem.text.strip()
                import re
                part_matches = re.findall(r'\b[A-Z0-9]{6,15}\b', text)
                for match in part_matches:
                    if len(match) >= 6:
                        parts.append({
                            'document_title': document_title,
                            'part_number': match,
                            'description': text[:100] + "..." if len(text) > 100 else text,
                            'chapter': "",
                            'section': "",
                            'figure': "",
                            'image_file': image_file,
                            'pdf_file': pdf_file,
                            'source_file': xml_file,
                            'category': category
                        })
    
    except Exception as e:
        print(f"Error parsing {xml_file}: {e}")
    
    return parts

def build_pdf_linked_database():
    """Build database with proper PDF linking"""
    base_dir = "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B"
    output_dir = f"{base_dir}_Extracted"
    
    print("=== CFM56-7B PDF-Linked Search Database ===")
    print("Building database with proper PDF document linking...")
    
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
    
    # Process each category
    for cat_key, cat_name in categories.items():
        print(f"\nProcessing {cat_name} ({cat_key})...")
        
        # Find XML files in this category
        xml_files = glob.glob(f"{base_dir}/datas/data/{cat_key}/7B/*.xml")
        print(f"  Found {len(xml_files)} XML files")
        
        # Extract parts with PDF links
        for xml_file in xml_files:
            parts = extract_parts_with_pdf_links(xml_file, cat_key)
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
    
    # Create database
    database = {
        'parts': all_parts,
        'documents': all_documents,
        'categories': categories,
        'stats': {
            'total_parts': len(all_parts),
            'total_documents': len(all_documents),
            'total_categories': len(categories)
        }
    }
    
    # Save database
    os.makedirs(output_dir, exist_ok=True)
    db_file = f"{output_dir}/pdf_linked_database.json"
    with open(db_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ PDF-linked database created!")
    print(f"   Database file: {db_file}")
    print(f"   Total parts: {len(all_parts)}")
    print(f"   Total documents: {len(all_documents)}")
    
    return database

def create_pdf_linked_search_viewer(database):
    """Create search viewer with proper PDF linking"""
    output_dir = "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B_Extracted"
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CFM56-7B PDF-Linked Search System</title>
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
            margin-bottom: 5px;
            text-decoration: none;
            display: block;
        }}
        .result-title:hover {{
            color: #1e3c72;
            text-decoration: underline;
        }}
        .result-part-number {{
            color: #666;
            font-size: 1em;
            margin-bottom: 10px;
            font-weight: 500;
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
        .action-button.pdf {{
            background: #dc3545;
            color: white;
            border-color: #dc3545;
        }}
        .action-button.pdf:hover {{
            background: #c82333;
        }}
        .action-button.image {{
            background: #28a745;
            color: white;
            border-color: #28a745;
        }}
        .action-button.image:hover {{
            background: #218838;
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
        .file-status {{
            font-size: 0.8em;
            color: #666;
            margin-top: 5px;
        }}
        .file-exists {{
            color: #28a745;
        }}
        .file-missing {{
            color: #dc3545;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>CFM56-7B PDF-Linked Search System</h1>
            <p>Search with direct access to PDF documents and images</p>
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
                <div class="stat-number">{database['stats']['total_categories']}</div>
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
                        document_title: part.document_title || 'Unknown Document',
                        part_number: part.part_number,
                        description: part.description || 'No description available',
                        details: `Category: ${{part.category}} | Chapter: ${{part.chapter}}-${{part.section}}-${{part.unit}} | Figure: ${{part.figure}}`,
                        category: part.category,
                        actions: getActionsForPart(part)
                    }});
                }} else if (part.description && part.description.toLowerCase().includes(query)) {{
                    results.push({{
                        type: 'part',
                        document_title: part.document_title || 'Unknown Document',
                        part_number: part.part_number || 'Unknown Part',
                        description: part.description,
                        details: `Category: ${{part.category}} | Chapter: ${{part.chapter}}-${{part.section}}-${{part.unit}} | Figure: ${{part.figure}}`,
                        category: part.category,
                        actions: getActionsForPart(part)
                    }});
                }} else if (part.document_title && part.document_title.toLowerCase().includes(query)) {{
                    results.push({{
                        type: 'part',
                        document_title: part.document_title,
                        part_number: part.part_number || 'Various parts',
                        description: part.description || 'No description available',
                        details: `Category: ${{part.category}} | Chapter: ${{part.chapter}}-${{part.section}}-${{part.unit}} | Figure: ${{part.figure}}`,
                        category: part.category,
                        actions: getActionsForPart(part)
                    }});
                }}
            }});
            
            displayResults(results);
        }}
        
        function getActionsForPart(part) {{
            const actions = [];
            
            // Add PDF link if available
            if (part.pdf_file) {{
                actions.push({{text: 'View PDF Document', url: `file://${{part.pdf_file}}`, class: 'pdf'}});
            }}
            
            // Add image link if available
            if (part.image_file) {{
                actions.push({{text: 'View Image', url: `file://${{part.image_file}}`, class: 'image'}});
            }}
            
            // Add source XML link
            if (part.source_file) {{
                actions.push({{text: 'View Source XML', url: `file://${{part.source_file}}`}});
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
                const pdfStatus = result.actions.some(a => a.class === 'pdf') ? 'file-exists' : 'file-missing';
                const imageStatus = result.actions.some(a => a.class === 'image') ? 'file-exists' : 'file-missing';
                
                // Get the main PDF link for the document title
                const pdfAction = result.actions.find(a => a.class === 'pdf');
                const titleLink = pdfAction ? pdfAction.url : '#';
                
                html += `
                    <div class="result-item">
                        <a href="${{titleLink}}" class="result-title" target="_blank">
                            ${{result.document_title || result.title}}
                            <span class="category-badge">${{result.category}}</span>
                        </a>
                        <div class="result-part-number">Part/Keyword: ${{result.part_number || 'N/A'}}</div>
                        <div class="result-description">${{result.description}}</div>
                        <div class="result-details">${{result.details}}</div>
                        <div class="file-status">
                            <span class="${{pdfStatus}}">PDF: ${{result.actions.some(a => a.class === 'pdf') ? 'Available' : 'Not found'}}</span> | 
                            <span class="${{imageStatus}}">Image: ${{result.actions.some(a => a.class === 'image') ? 'Available' : 'Not found'}}</span>
                        </div>
                        <div class="result-actions">
                            ${{result.actions.map(action => 
                                `<a href="${{action.url}}" class="action-button ${{action.class || ''}}" target="_blank">${{action.text}}</a>`
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
    with open(f"{output_dir}/pdf_linked_search.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"PDF-linked search viewer created: {output_dir}/pdf_linked_search.html")
    return f"{output_dir}/pdf_linked_search.html"

def main():
    print("=== CFM56-7B PDF-Linked Search System ===")
    
    # Build database with PDF linking
    database = build_pdf_linked_database()
    
    # Create PDF-linked search viewer
    html_file = create_pdf_linked_search_viewer(database)
    
    print(f"\n✅ PDF-linked search system created!")
    print(f"   Search system: {html_file}")
    print(f"\nFeatures:")
    print(f"   - Direct links to PDF documents")
    print(f"   - Direct links to images")
    print(f"   - {database['stats']['total_parts']} parts with PDF mapping")
    print(f"   - {database['stats']['total_documents']} PDF documents")
    print(f"   - No more XML-only results!")

if __name__ == "__main__":
    main()
