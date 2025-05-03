#!/bin/bash

# SafeWayAI Mobile App Builder
echo "SafeWayAI Mobile App Builder"
echo "==========================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    exit 1
fi

# Check if Flet is installed
if ! python3 -c "import flet" &> /dev/null; then
    echo "Installing Flet..."
    pip install flet
fi

# Check if API keys are configured
if [ ! -f "assets/.env" ]; then
    echo "API keys are not configured. Running the API key generator..."
    python3 generate_api_keys.py
fi

# Build the Android APK
echo ""
echo "Building Android APK..."
flet build apk --module-name main_flet.py

# Check if the build was successful
if [ -f "build/flutter/build/app/outputs/apk/release/app-release.apk" ]; then
    echo ""
    echo "Android APK built successfully!"
    echo "APK location: build/flutter/build/app/outputs/apk/release/app-release.apk"
    echo ""
    echo "To install on an Android device, run: ./install_safewayai.sh"
else
    echo ""
    echo "Android APK build failed. Please check the error messages above."
fi

# Check if we're on macOS for iOS build
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo ""
    echo "Building iOS IPA..."
    flet build ipa --module-name main_flet.py
    
    # Check if the build was successful
    if [ -d "build/flutter/ios/Runner.xcworkspace" ]; then
        echo ""
        echo "iOS project built successfully!"
        echo "Open the Xcode project: open build/flutter/ios/Runner.xcworkspace"
        echo "Then build and archive the app in Xcode."
    else
        echo ""
        echo "iOS project build failed. Please check the error messages above."
    fi
else
    echo ""
    echo "iOS build is only available on macOS."
    echo "To build for iOS, transfer this project to a Mac and run this script there."
fi

echo ""
echo "Build process completed!"
