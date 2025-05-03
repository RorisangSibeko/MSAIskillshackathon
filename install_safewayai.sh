#!/bin/bash

# SafeWayAI Installation Script
echo "SafeWayAI Installation Script"
echo "============================"
echo ""

APK_PATH="/home/wethinkcode_/SafeWayAI/build/flutter/build/app/outputs/apk/release/app-release.apk"

if [ ! -f "$APK_PATH" ]; then
    echo "Error: APK file not found at $APK_PATH"
    exit 1
fi

echo "APK file found: $APK_PATH"
echo ""

# Check if adb is installed
if ! command -v adb &> /dev/null; then
    echo "Error: adb (Android Debug Bridge) is not installed."
    echo "Please install Android SDK platform tools to continue."
    echo "You can install it using: sudo apt install adb"
    exit 1
fi

# Check for connected devices
echo "Checking for connected Android devices..."
DEVICES=$(adb devices | grep -v "List" | grep "device" | wc -l)

if [ "$DEVICES" -eq 0 ]; then
    echo "No Android devices found. Please connect your device and enable USB debugging."
    echo "Instructions:"
    echo "1. Enable Developer Options on your Android device by tapping 'Build Number' 7 times in Settings > About Phone"
    echo "2. Enable USB Debugging in Settings > Developer Options"
    echo "3. Connect your device to this computer via USB"
    echo "4. Allow USB debugging when prompted on your device"
    exit 1
fi

echo "Found $DEVICES Android device(s) connected."
echo ""

# Install the APK
echo "Installing SafeWayAI on your device..."
adb install -r "$APK_PATH"

if [ $? -eq 0 ]; then
    echo ""
    echo "SafeWayAI has been successfully installed on your device!"
    echo "You can now open the app from your app drawer."
else
    echo ""
    echo "Installation failed. Please try again or install manually."
fi
