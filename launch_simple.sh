#!/bin/bash
# Simple CFM56-7B Launcher - tries to bypass native library issues

echo "Starting CFM56-7B Nomad Application (Simple Mode)..."
echo "Please wait while the application loads..."

# Change to the application directory
cd "$(dirname "$0")"

# Try running with minimal options to avoid native library conflicts
echo "Attempting to launch with minimal Java options..."
java -Djava.awt.headless=false \
     -Djava.library.path="" \
     -Dsun.java2d.noddraw=true \
     -Dsun.java2d.d3d=false \
     -Dsun.java2d.opengl=false \
     -Dsun.java2d.pmoffscreen=false \
     -Dsun.java2d.xrender=false \
     -Djava.awt.printerjob=sun.print.PSPrinterJob \
     -Xmx512m -Xms128m \
     -jar Nomad.jar 2>&1

echo "Application closed."
