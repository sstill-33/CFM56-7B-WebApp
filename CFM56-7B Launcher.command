#!/bin/bash
# CFM56-7B Launcher for macOS
# Double-click this file to launch the application

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the application directory
cd "$DIR"

# Launch the application with the working configuration
./launch_final.sh
