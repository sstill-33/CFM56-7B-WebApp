#!/usr/bin/env python3
"""
Fix document naming conventions in the search database
Extracts proper document titles from PDF filenames
"""

import os
import json
import glob
import re
import xml.etree.ElementTree as ET

def extract_document_title_from_filename(pdf_file, category):
    """Extract proper document title from PDF filename"""
    if not pdf_file:
        return f"{category} Unknown Document"
    
    pdf_basename = os.path.splitext(os.path.basename(pdf_file))[0]
    
    if category == "SB":
        # For Service Bulletins, look for pattern like "72-05-32"
        sb_match = re.search(r'(\d{2}-\d{2}-\d{2})', pdf_basename)
        if sb_match:
            return f"SB {sb_match.group(1)}"
        else:
            return f"SB {pdf_basename}"
    
    elif category == "ESM":
        # For ESM, look for pattern like "72-55-15-300-006-A-00-PGK-09-006-NA"
        esm_match = re.search(r'(\d{2}-\d{2}-\d{2}-\d{3}-\d{3}-[A-Z]-\d{2}-[A-Z]{3}-\d{2}-\d{3}-[A-Z]{2})', pdf_basename)
        if esm_match:
            return f"ESM {esm_match.group(1)}"
        else:
            # Try to extract any meaningful pattern
            parts_split = pdf_basename.split('_')
            if len(parts_split) > 1:
                return f"ESM {parts_split[-1]}"
            else:
                return f"ESM {pdf_basename}"
    
    elif category == "EIPC":
        # For EIPC, look for pattern like "72-00-00-01"
        eipc_match = re.search(r'(\d{2}-\d{2}-\d{2}-\d{2})', pdf_basename)
        if eipc_match:
            return f"EIPC {eipc_match.group(1)}"
        else:
            parts_split = pdf_basename.split('_')
            if len(parts_split) > 1:
                return f"EIPC {parts_split[-1]}"
            else:
                return f"EIPC {pdf_basename}"
    
    else:
        # For other categories, use the last meaningful part
        parts_split = pdf_basename.split('_')
        if len(parts_split) > 1:
            return f"{category} {parts_split[-1]}"
        else:
            return f"{category} {pdf_basename}"

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

def extract_parts_with_proper_naming(xml_file, category):
    """Extract parts with proper document naming"""
    parts = []
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Find the corresponding PDF
        pdf_file = find_pdf_for_xml(xml_file, category)
        image_file = find_image_for_xml(xml_file, category)
        
        # Get proper document title from PDF filename
        document_title = extract_document_title_from_filename(pdf_file, category)
        
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

def rebuild_database_with_proper_naming():
    """Rebuild the database with proper document naming"""
    base_dir = "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B"
    output_dir = f"{base_dir}_Extracted"
    
    print("=== Rebuilding Database with Proper Document Naming ===")
    print("Extracting document titles from PDF filenames...")
    
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
        
        # Extract parts with proper naming
        for xml_file in xml_files:
            parts = extract_parts_with_proper_naming(xml_file, cat_key)
            all_parts.extend(parts)
        
        # Find PDF files in this category
        pdf_files = glob.glob(f"{base_dir}/datas/data/{cat_key}/7B/*.pdf")
        print(f"  Found {len(pdf_files)} PDF files")
        
        for pdf_file in pdf_files:
            document_title = extract_document_title_from_filename(pdf_file, cat_key)
            all_documents.append({
                'name': os.path.basename(pdf_file),
                'title': document_title,
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
    db_file = f"{output_dir}/pdf_linked_database_fixed.json"
    with open(db_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Fixed database created!")
    print(f"   Database file: {db_file}")
    print(f"   Total parts: {len(all_parts)}")
    print(f"   Total documents: {len(all_documents)}")
    
    # Show some examples
    print(f"\n📋 Sample document titles:")
    for i, doc in enumerate(all_documents[:10]):
        print(f"   {i+1}. {doc['title']}")
    
    return database

def update_webapp_database():
    """Update the webapp database with fixed naming"""
    base_dir = "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B"
    source_db = f"{base_dir}_Extracted/pdf_linked_database_fixed.json"
    target_db = f"{base_dir}/CFM56-7B_WebApp/data/pdf_linked_database.json"
    
    if os.path.exists(source_db):
        import shutil
        shutil.copy2(source_db, target_db)
        print(f"✅ Updated webapp database: {target_db}")
    else:
        print(f"❌ Source database not found: {source_db}")

def main():
    print("=== CFM56-7B Document Naming Fix ===")
    
    # Rebuild database with proper naming
    database = rebuild_database_with_proper_naming()
    
    # Update webapp database
    update_webapp_database()
    
    print(f"\n✅ Document naming fixed!")
    print(f"   - Service Bulletins now show as 'SB 72-05-32'")
    print(f"   - ESM now shows as 'ESM 72-55-15-300-006-A-00-PGK-09-006-NA'")
    print(f"   - EIPC now shows as 'EIPC 72-00-00-01'")
    print(f"   - Other categories follow similar patterns")

if __name__ == "__main__":
    main()
