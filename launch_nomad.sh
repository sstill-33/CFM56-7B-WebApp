#!/bin/bash
# CFM56-7B Nomad Launcher for macOS
# This script launches the Nomad application with proper Java settings

echo "Starting CFM56-7B Nomad Application..."
echo "Please wait while the application loads..."

# Change to the application directory
cd "$(dirname "$0")"

# Use system Java with options to bypass native library issues
echo "Using system Java with compatibility options..."
java -Djava.awt.headless=false \
     -Djava.library.path="" \
     -Djava.awt.graphicsenv=sun.awt.X11GraphicsEnvironment \
     -Dsun.java2d.noddraw=true \
     -Dsun.java2d.d3d=false \
     -Dsun.java2d.opengl=false \
     -Dsun.java2d.pmoffscreen=false \
     -Xmx512m -Xms128m \
     -jar Nomad.jar

echo "Application closed."
