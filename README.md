# MSAIskillshackathon - SafeWayAI

# SafeWayAI - AI-Powered Emergency Detection & Response System

SafeWayAI is a real-time, AI-powered safety and emergency detection platform designed to enhance security in high-risk environments such as homes, schools, industrial sites, hospitals, or public spaces.

## Overview

The system uses AI simulation to monitor live camera feeds and detect potentially dangerous or emergency scenarios such as fire, accidents, or abnormal behavior, and immediately alerts the relevant authorities or internal emergency response systems.

Built using Python and the Kivy framework, SafeWayAI provides a smooth and interactive cross-platform user interface. It aims to bring smart safety monitoring to institutions with a modular and extendable design, laying the groundwork for integrating real AI/ML detection algorithms in future iterations.

## Key Features

1. **AI Monitoring Screen**
   - Simulates AI-based monitoring of environments
   - Automatically checks for emergencies at regular intervals
   - Triggers alerts when an emergency is detected

2. **Emergency Alert System**
   - Displays emergency alerts on a dedicated screen
   - Central hub for managing detected alerts
   - Can be extended to support push notifications, SMS, or emails

3. **Incident History Logging**
   - Logs all past alerts with timestamps
   - Enables review and audit of historical emergency events
   - Useful for analytics and security audits

4. **Manual Reporting**
   - Allows users to manually report emergencies
   - Bypasses automated detection for user-initiated alerts

5. **Settings and Customization**
   - Enables control over alert sensitivity, timer intervals, and user preferences
   - UI customization options for color themes and layout

6. **User Authentication and Roles**
   - Admin, responder, and viewer roles
   - Access controls based on roles

7. **Scalability & AI Integration Ready**
   - Designed with modules that allow easy integration of real AI/ML models
   - Future-proof architecture for live feed analysis

## Project Structure

```
SafeWayAI/
│
├── app/                              # Main application code
│   ├── main.py                       # Main app launcher and core classes
│   └── safewayai.kv                  # Kivy UI definitions
│
├── services/                         # Service modules
│   ├── panic_detector.py             # Emergency detection logic
│   ├── mock_maps.py                  # Location-based risk assessment
│   └── mock_speech.py                # Speech recognition simulation
│
├── tests/                            # Unit tests
│   ├── test_safewayai.py             # Tests for core functionality
│   └── test_panic.py                 # Tests for panic detection
│
├── assets/                           # Icons, sounds, media
│   └── icons/
│       ├── app_icon.png
│       ├── ai_monitoring.png
│       └── presplash.png
│
├── data/                             # Data storage (created at runtime)
│   ├── incidents.json                # Stored incident history
│   ├── settings.json                 # User settings
│   └── users.json                    # User accounts
│
├── screens/                          # KV files for individual screens
│   └── home.kv                       # Home screen definition
│
└── README.md                         # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/SafeWayAI.git
   cd SafeWayAI
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Initialize the secure vault (first-time setup only):
   ```
   python app/utils/initialize_vault.py
   ```
   This will prompt you to create a password for the vault and securely store the Azure credentials.

4. Run the application:
   ```
   python app/main.py
   ```

## Secure Vault

SafeWayAI uses a secure vault to protect sensitive credentials such as API keys and connection strings. The vault encrypts all credentials using a password-derived key and stores them in an encrypted file.

### How it works

1. The vault uses the cryptography library to encrypt and decrypt credentials
2. Credentials are stored in an encrypted file (vault.enc) with a separate salt file (salt.bin)
3. The vault is unlocked using a password, which can be provided via:
   - Interactive prompt
   - Environment variable (SAFEWAYAI_VAULT_PASSWORD)
   - .env file in the app/assets directory

### Managing credentials

- To initialize the vault with credentials: `python app/utils/initialize_vault.py`
- To test the vault: `python test_vault.py`

## Default User Accounts

The application comes with three default user accounts:

- **Admin**
  - Username: admin
  - Password: admin123
  - Role: admin
  - Permissions: Full access to all features

- **Responder**
  - Username: responder
  - Password: respond123
  - Role: responder
  - Permissions: Can view monitoring, report emergencies, and clear alerts

- **Viewer**
  - Username: viewer
  - Password: view123
  - Role: viewer
  - Permissions: Can only view monitoring and incident history

## Mobile Deployment

The mobile deployment files are available in the `mobile_deployment` branch of this repository. This branch contains all the necessary files for deploying the SafeWayAI application to iOS and Android devices.

### Files Included in Mobile Deployment Branch

- **DEPLOYMENT_GUIDE.md**: Comprehensive guide on how to deploy the app to iOS and Android
- **MOBILE_README.md**: README file for the mobile app with installation instructions
- **build_mobile_app.sh**: Script to build the app for both Android and iOS platforms
- **generate_api_keys.py**: Script to guide users through generating the necessary Azure API keys
- **install_safewayai.sh**: Script to help install the APK on Android devices

### Getting Started with Mobile Deployment

1. Switch to the mobile_deployment branch:
   ```bash
   git checkout mobile_deployment
   ```

2. Build the app:
   ```bash
   ./build_mobile_app.sh
   ```

3. Install on Android:
   ```bash
   ./install_safewayai.sh
   ```

4. For iOS deployment, follow the instructions in the DEPLOYMENT_GUIDE.md file.

## Testing

Run the tests with:

```
cd tests
python -m unittest discover
```

## Future Enhancements

- Integration with real AI models using camera feeds
- Voice command emergency reporting
- Cloud-based alert syncing and remote admin access
- SMS/Email push notifications
- iOS deployment

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Kivy framework for the cross-platform UI
- Python community for the excellent libraries

