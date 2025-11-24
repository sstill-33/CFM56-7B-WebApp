#!/bin/bash
# CFM56-7B Complete System Launcher
# This gives you access to all the different viewers and search systems

echo "=== CFM56-7B Aviation Maintenance System ==="
echo "Choose your preferred interface:"
echo ""
echo "1. PDF-Linked Search System (Recommended)"
echo "   - Direct links to PDF documents"
echo "   - Direct links to images"
echo "   - 361,112 parts with PDF mapping"
echo "   - No more XML-only results!"
echo ""
echo "2. Comprehensive Search System"
echo "   - Search across ALL 11 categories"
echo "   - 361,112 parts and references"
echo "   - 7,802 PDF documents"
echo "   - 2,673 service bulletins"
echo "   - Filter by category"
echo ""
echo "3. Enhanced Search System (EIPC Focus)"
echo "   - Search by part numbers"
echo "   - Search by keywords"
echo "   - Part number to image linking"
echo "   - 23,609 part numbers indexed"
echo ""
echo "4. Document Browser"
echo "   - Browse by category"
echo "   - 7,802 PDF documents"
echo "   - 11 document categories"
echo ""
echo "5. Open all systems"
echo ""
echo "Enter your choice (1, 2, 3, 4, or 5):"

read choice

case $choice in
    1)
        echo "Opening PDF-Linked Search System..."
        open "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B_Extracted/pdf_linked_search.html"
        ;;
    2)
        echo "Opening Comprehensive Search System..."
        open "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B_Extracted/comprehensive_search.html"
        ;;
    3)
        echo "Opening Enhanced Search System..."
        open "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B_Extracted/enhanced_search.html"
        ;;
    4)
        echo "Opening Document Browser..."
        open "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B_Extracted/index.html"
        ;;
    5)
        echo "Opening all systems..."
        open "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B_Extracted/pdf_linked_search.html"
        open "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B_Extracted/comprehensive_search.html"
        open "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B_Extracted/enhanced_search.html"
        open "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B_Extracted/index.html"
        ;;
    *)
        echo "Invalid choice. Opening PDF-Linked Search System by default..."
        open "/Users/stevenstill/Desktop/Programming/Cursor Apps/EM/CFM56-7B_Extracted/pdf_linked_search.html"
        ;;
esac

echo ""
echo "System opened! You now have access to:"
echo "• 361,112 parts and references across ALL categories"
echo "• 7,802 PDF documents organized by category"
echo "• 2,673 service bulletins with full search"
echo "• 11 document categories (EIPC, ESM, SB, CMM, CPM, ITEM, NDTM, LLP, SOLUTIONS, SPM, TSP)"
echo "• Advanced filtering and search capabilities"
echo "• Direct links to source files and images"
echo ""
echo "The original Windows application has been completely replaced"
echo "with a modern, comprehensive macOS-compatible system!"
