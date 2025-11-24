#!/bin/bash
# Final CFM56-7B Launcher - optimized for macOS compatibility

echo "Starting CFM56-7B Nomad Application..."
echo "Please wait while the application loads..."

# Change to the application directory
cd "$(dirname "$0")"

# Run with macOS-optimized settings
echo "Launching with macOS-optimized Java settings..."
java -Djava.awt.headless=false \
     -Djava.library.path="" \
     -Dsun.java2d.noddraw=true \
     -Dsun.java2d.d3d=false \
     -Dsun.java2d.opengl=false \
     -Dsun.java2d.pmoffscreen=false \
     -Dsun.java2d.xrender=false \
     -Djava.awt.printerjob=sun.print.PSPrinterJob \
     -Dapple.laf.useScreenMenuBar=true \
     -Dcom.apple.macos.useScreenMenuBar=true \
     -Dcom.apple.mrj.application.apple.menu.about.name="CFM56-7B Nomad" \
     -Xmx512m -Xms128m \
     -jar Nomad.jar

echo "Application closed."
