#!/bin/bash
# CFM56-7B Document Extraction and Organization Script
# This script extracts all documents and creates an organized structure

echo "=== CFM56-7B Document Extraction and Organization ==="
echo "Starting extraction process..."

# Create main output directory
OUTPUT_DIR="/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B_Extracted"
mkdir -p "$OUTPUT_DIR"

# Create category directories
echo "Creating directory structure..."
mkdir -p "$OUTPUT_DIR/01_PDFs/EIPC"
mkdir -p "$OUTPUT_DIR/01_PDFs/ESM" 
mkdir -p "$OUTPUT_DIR/01_PDFs/SB"
mkdir -p "$OUTPUT_DIR/01_PDFs/CMM"
mkdir -p "$OUTPUT_DIR/01_PDFs/CPM"
mkdir -p "$OUTPUT_DIR/01_PDFs/ITEM"
mkdir -p "$OUTPUT_DIR/01_PDFs/NDTM"
mkdir -p "$OUTPUT_DIR/01_PDFs/LLP"
mkdir -p "$OUTPUT_DIR/01_PDFs/SOLUTIONS"
mkdir -p "$OUTPUT_DIR/01_PDFs/SPM"
mkdir -p "$OUTPUT_DIR/01_PDFs/TSP"
mkdir -p "$OUTPUT_DIR/02_Images"
mkdir -p "$OUTPUT_DIR/03_XML_Documents"
mkdir -p "$OUTPUT_DIR/04_Index_Files"

# Extract PDFs by category
echo "Extracting PDFs by category..."

# EIPC PDFs
echo "Extracting EIPC PDFs..."
find "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B/datas/data/EIPC" -name "*.pdf" -exec cp {} "$OUTPUT_DIR/01_PDFs/EIPC/" \;

# ESM PDFs  
echo "Extracting ESM PDFs..."
find "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B/datas/data/ESM" -name "*.pdf" -exec cp {} "$OUTPUT_DIR/01_PDFs/ESM/" \;

# SB PDFs
echo "Extracting SB PDFs..."
find "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B/datas/data/SB" -name "*.pdf" -exec cp {} "$OUTPUT_DIR/01_PDFs/SB/" \;

# CMM PDFs
echo "Extracting CMM PDFs..."
find "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B/datas/data/CMM" -name "*.pdf" -exec cp {} "$OUTPUT_DIR/01_PDFs/CMM/" \;

# CPM PDFs
echo "Extracting CPM PDFs..."
find "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B/datas/data/CPM" -name "*.pdf" -exec cp {} "$OUTPUT_DIR/01_PDFs/CPM/" \;

# ITEM PDFs
echo "Extracting ITEM PDFs..."
find "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B/datas/data/ITEM" -name "*.pdf" -exec cp {} "$OUTPUT_DIR/01_PDFs/ITEM/" \;

# NDTM PDFs
echo "Extracting NDTM PDFs..."
find "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B/datas/data/NDTM" -name "*.pdf" -exec cp {} "$OUTPUT_DIR/01_PDFs/NDTM/" \;

# LLP PDFs
echo "Extracting LLP PDFs..."
find "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B/datas/data/LLP" -name "*.pdf" -exec cp {} "$OUTPUT_DIR/01_PDFs/LLP/" \;

# SOLUTIONS PDFs
echo "Extracting SOLUTIONS PDFs..."
find "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B/datas/data/SOLUTIONS" -name "*.pdf" -exec cp {} "$OUTPUT_DIR/01_PDFs/SOLUTIONS/" \;

# SPM PDFs
echo "Extracting SPM PDFs..."
find "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B/datas/data/SPM" -name "*.pdf" -exec cp {} "$OUTPUT_DIR/01_PDFs/SPM/" \;

# TSP PDFs
echo "Extracting TSP PDFs..."
find "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B/datas/data/TSP" -name "*.pdf" -exec cp {} "$OUTPUT_DIR/01_PDFs/TSP/" \;

# Extract images
echo "Extracting technical images..."
find "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B/datas/art" -name "*.tif" -o -name "*.png" -o -name "*.svg" | head -1000 | xargs -I {} cp {} "$OUTPUT_DIR/02_Images/"

# Extract XML documents
echo "Extracting XML documents..."
find "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B/datas/arbo" -name "*.xml" -exec cp {} "$OUTPUT_DIR/03_XML_Documents/" \;

# Copy index files
echo "Copying index files..."
cp "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B/datas/sbindex.csv" "$OUTPUT_DIR/04_Index_Files/"
cp "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B/datas/sbindex.json" "$OUTPUT_DIR/04_Index_Files/"
cp "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B/datas/catalog.xml" "$OUTPUT_DIR/04_Index_Files/"

echo "Extraction complete!"
echo "Documents organized in: $OUTPUT_DIR"
