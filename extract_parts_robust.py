#!/usr/bin/env python3
"""
Robust Part Number Extraction for CFM56-7B
Uses a different approach to extract part numbers without getparent()
"""

import os
import json
import xml.etree.ElementTree as ET
import glob
import re

def extract_parts_robust(xml_file):
    """Extract part numbers using a robust approach"""
    parts = []
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Find all item elements that contain part numbers
        for item in root.findall('.//item'):
            part_info = {}
            
            # Extract part number
            pnr_elem = item.find('.//pnr')
            if pnr_elem is not None and pnr_elem.text:
                part_info['part_number'] = pnr_elem.text
                
                # Extract description from nom element
                nom_elem = item.find('.//nom')
                if nom_elem is not None:
                    kwd = nom_elem.find('kwd')
                    adt = nom_elem.find('adt')
                    if kwd is not None and adt is not None:
                        part_info['description'] = f"{kwd.text} {adt.text}".strip()
                    elif kwd is not None:
                        part_info['description'] = kwd.text
                
                # Extract chapter/section info from item attributes
                part_info['chapter'] = item.get('chapnbr', '')
                part_info['section'] = item.get('sectnbr', '')
                part_info['unit'] = item.get('unitnbr', '')
                part_info['figure'] = item.get('fignbr', '')
                part_info['item'] = item.get('itemnbr', '')
                
                # Extract manufacturer
                mfr_elem = item.find('.//mfr')
                if mfr_elem is not None:
                    part_info['manufacturer'] = mfr_elem.text
                
                # Extract service bulletin references
                sbnbr_elem = item.find('.//sbnbr')
                if sbnbr_elem is not None:
                    part_info['service_bulletin'] = sbnbr_elem.text
                    part_info['sb_file'] = sbnbr_elem.get('uncfile', '')
                
                # Find associated image file in the same document
                for sheet in root.findall('.//sheet'):
                    uncfile = sheet.get('uncfile', '')
                    if uncfile:
                        part_info['image_file'] = uncfile
                        break
                
                part_info['source_file'] = xml_file
                parts.append(part_info)
    
    except Exception as e:
        print(f"Error parsing {xml_file}: {e}")
    
    return parts

def build_comprehensive_parts_database():
    """Build a comprehensive parts database"""
    base_dir = "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B"
    output_dir = f"{base_dir}_Extracted"
    
    print("Building comprehensive parts database...")
    
    all_parts = []
    
    # Extract from EIPC files
    print("Extracting from EIPC files...")
    eipc_files = glob.glob(f"{base_dir}/datas/data/EIPC/7B/*.xml")
    for xml_file in eipc_files:
        parts = extract_parts_robust(xml_file)
        for part in parts:
            part['category'] = 'EIPC'
            all_parts.append(part)
    
    # Extract from ESM files
    print("Extracting from ESM files...")
    esm_files = glob.glob(f"{base_dir}/datas/data/ESM/7B/*.xml")
    for xml_file in esm_files:
        parts = extract_parts_robust(xml_file)
        for part in parts:
            part['category'] = 'ESM'
            all_parts.append(part)
    
    # Extract from SB files
    print("Extracting from SB files...")
    sb_files = glob.glob(f"{base_dir}/datas/data/SB/7B/*.xml")
    for xml_file in sb_files:
        parts = extract_parts_robust(xml_file)
        for part in parts:
            part['category'] = 'SB'
            all_parts.append(part)
    
    # Save parts database
    parts_file = f"{output_dir}/parts_database.json"
    with open(parts_file, 'w', encoding='utf-8') as f:
        json.dump(all_parts, f, indent=2, ensure_ascii=False)
    
    print(f"Parts database created: {parts_file}")
    print(f"Total parts extracted: {len(all_parts)}")
    
    # Show sample parts
    if all_parts:
        print("\nSample parts:")
        for i, part in enumerate(all_parts[:5]):
            print(f"  {i+1}. {part.get('part_number', 'N/A')} - {part.get('description', 'No description')}")
    
    return all_parts

def create_enhanced_search_viewer(parts_db):
    """Create an enhanced search viewer with the parts database"""
    output_dir = "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B_Extracted"
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CFM56-7B Enhanced Search System</title>
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
        .part-highlight {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            border-radius: 4px;
            margin: 15px 0;
        }}
        .category-badge {{
            display: inline-block;
            padding: 4px 8px;
            background: #e3f2fd;
            color: #1976d2;
            border-radius: 12px;
            font-size: 0.8em;
            margin-right: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>CFM56-7B Enhanced Search System</h1>
            <p>Search by part numbers, keywords, or document titles</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(parts_db)}</div>
                <div class="stat-label">Part Numbers</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">7,802</div>
                <div class="stat-label">Documents</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">10,963</div>
                <div class="stat-label">Images</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">2,029</div>
                <div class="stat-label">Service Bulletins</div>
            </div>
        </div>
        
        <div class="search-section">
            <div class="search-container">
                <input type="text" id="searchInput" class="search-input" placeholder="Enter part number, keyword, or document title..." onkeyup="handleSearch()">
                <button onclick="performSearch()" class="search-button">Search</button>
            </div>
        </div>
        
        <div class="results-section">
            <div id="searchResults">
                <div class="no-results">
                    <h3>Enter a search term to find parts, documents, or service bulletins</h3>
                    <p>Try searching for part numbers or keywords</p>
                    <div class="part-highlight">
                        <strong>Sample Part Numbers:</strong><br>
                        {', '.join([part.get('part_number', '') for part in parts_db[:10] if part.get('part_number')])}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const partsDatabase = {json.dumps(parts_db, indent=2)};
        
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
            
            // Search parts
            partsDatabase.forEach(part => {{
                if (part.part_number && part.part_number.toLowerCase().includes(query)) {{
                    results.push({{
                        type: 'part',
                        title: part.part_number,
                        description: part.description || 'No description available',
                        details: `Chapter: ${{part.chapter}}-${{part.section}}-${{part.unit}} | Figure: ${{part.figure}} | Category: ${{part.category}}`,
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
                        details: `Chapter: ${{part.chapter}}-${{part.section}}-${{part.unit}} | Figure: ${{part.figure}} | Category: ${{part.category}}`,
                        actions: [
                            {{text: 'View Document', url: `file://${{part.source_file}}`}},
                            {{text: 'View Image', url: `file://${{part.image_file}}`}}
                        ]
                    }});
                }}
            }});
            
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
                    <p>Try searching for part numbers, keywords, or document titles</p>
                </div>
            `;
        }}
    </script>
</body>
</html>
"""
    
    # Write the HTML file
    with open(f"{output_dir}/enhanced_search.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Enhanced search viewer created: {output_dir}/enhanced_search.html")
    return f"{output_dir}/enhanced_search.html"

def main():
    print("=== CFM56-7B Robust Parts Extraction ===")
    
    # Build parts database
    parts_db = build_comprehensive_parts_database()
    
    # Create enhanced search viewer
    html_file = create_enhanced_search_viewer(parts_db)
    
    print(f"\n✅ Enhanced search system created!")
    print(f"   Enhanced search: {html_file}")
    print(f"\nFeatures:")
    print(f"   - Search by part numbers")
    print(f"   - Search by part descriptions")
    print(f"   - Direct links to source documents")
    print(f"   - Direct links to associated images")
    print(f"   - Part number to image linking")

if __name__ == "__main__":
    main()
