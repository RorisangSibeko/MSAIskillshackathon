# SafeWayAI Deployment Guide

This guide provides instructions on how to deploy the SafeWayAI application to iOS and Android devices.

## Android Deployment

### Option 1: Direct Installation (Development)

1. Connect your Android device to your computer via USB
2. Enable USB debugging on your Android device:
   - Go to Settings > About Phone
   - Tap "Build Number" 7 times to enable Developer Options
   - Go to Settings > Developer Options
   - Enable "USB Debugging"
3. Run the installation script:
   ```bash
   ./install_safewayai.sh
   ```
4. The app will be installed on your device and can be launched from the app drawer

### Option 2: Google Play Store (Production)

To distribute the app through the Google Play Store:

1. Create a Google Play Developer account ($25 one-time fee)
2. Sign the APK with a release key:
   ```bash
   keytool -genkey -v -keystore safewayai-release-key.keystore -alias safewayai -keyalg RSA -keysize 2048 -validity 10000
   ```
3. Use the signed APK to upload to the Google Play Console
4. Fill in the app details, screenshots, and descriptions
5. Submit for review

## iOS Deployment

iOS deployment requires a macOS computer with Xcode installed.

### Prerequisites

1. Mac computer with macOS 10.15 or later
2. Xcode 12 or later
3. Apple Developer account ($99/year)
4. iOS device for testing (optional)

### Steps for iOS Deployment

1. Transfer the SafeWayAI project to the Mac
2. Install Flutter on the Mac:
   ```bash
   brew install flutter
   ```
3. Run the Flet build command for iOS:
   ```bash
   cd /path/to/SafeWayAI
   flet build ipa --module-name main_flet.py
   ```
4. Open the generated Xcode project:
   ```bash
   open build/flutter/ios/Runner.xcworkspace
   ```
5. In Xcode:
   - Select your development team
   - Configure app signing
   - Set the bundle identifier
6. Build and archive the app in Xcode
7. Use App Store Connect to submit the app for review

### TestFlight Distribution (Beta Testing)

1. Archive the app in Xcode
2. Upload to App Store Connect
3. Configure TestFlight settings
4. Add testers via email or public link

## App Size Optimization

The current APK size is large (1.3GB) due to including the Python interpreter and all dependencies. To reduce the size:

1. Use the `--cleanup-packages` flag when building:
   ```bash
   flet build apk --module-name main_flet.py --cleanup-packages
   ```
2. Split the APK by architecture:
   ```bash
   flet build apk --module-name main_flet.py --split-per-abi
   ```
3. Remove unnecessary dependencies from requirements.txt

## Troubleshooting

### Android Installation Issues

- If the app fails to install, check that:
  - USB debugging is enabled
  - You have sufficient storage space on your device
  - You've allowed installation from unknown sources

### iOS Deployment Issues

- If Xcode signing fails:
  - Verify your Apple Developer account is active
  - Check that your provisioning profile is valid
  - Ensure the bundle identifier is unique

## API Keys and Configuration

The app requires various Azure API keys to function properly. These should be configured:

1. Create a `.env` file in the app's assets directory with your API keys
2. The app will load these keys at runtime
3. For production, consider using a secure storage solution

For any issues or questions, please contact the SafeWayAI development team.
