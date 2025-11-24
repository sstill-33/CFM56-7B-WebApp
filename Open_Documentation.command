#!/bin/bash
# CFM56-7B Documentation Viewer Launcher
# This opens the HTML-based documentation viewer

echo "Opening CFM56-7B Documentation Viewer..."

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Open the HTML viewer
open "$DIR/CFM56-7B_Extracted/index.html"

echo "Documentation viewer opened in your default browser!"
echo "You now have access to all 7,802 PDF documents organized by category."
