# SafeWayAI - AI-Powered Emergency Detection & Response System

SafeWayAI is a real-time, AI-powered safety and emergency detection platform designed to enhance security in high-risk environments such as homes, schools, industrial sites, hospitals, or public spaces.

## Overview

The system uses AI simulation to monitor live camera feeds and detect potentially dangerous or emergency scenarios such as fire, accidents, or abnormal behavior, and immediately alerts the relevant authorities or internal emergency response systems.

Built using Python and the Flet framework (which uses Flutter), SafeWayAI provides a smooth and interactive cross-platform user interface. It aims to bring smart safety monitoring to institutions with a modular and extendable design, laying the groundwork for integrating real AI/ML detection algorithms in future iterations.

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

7. **Subscription Model**
   - Basic free tier with limited features
   - Premium subscription with advanced safety features
   - Enterprise plans for businesses, schools, and organizations

8. **IoT Integration**
   - Connect with smart home devices, security systems, and wearables
   - Automated emergency protocols
   - Health monitoring for medical emergencies

9. **Insurance Company Integration**
   - Discounts on insurance premiums for users
   - Data sharing capabilities (with user consent) for risk assessment
   - Custom white-label versions for insurance companies

10. **GBV Prevention Features**
    - Quick access to support resources
    - Pattern recognition for recurring threats
    - Document storage for legal protection
    - Safety planning and risk assessment

## Economic Viability

SafeWayAI is designed to be economically viable through multiple revenue streams:

1. **Subscription Revenue**
   - Tiered subscription model (Basic, Standard, Premium, Enterprise)
   - Monthly and annual billing options with discounts for annual commitments

2. **Insurance Partnerships**
   - Revenue sharing with insurance companies
   - Referral fees for new insurance customers
   - Premium discounts for SafeWayAI users

3. **Security System Integration**
   - Commission-based referrals to security installation companies
   - API licensing for security system manufacturers
   - Value-added services for existing security systems

4. **Enterprise Solutions**
   - Custom deployments for businesses, schools, and organizations
   - API access for custom integrations
   - White-label solutions for partners

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

3. Run the application:
   ```
   python main_flet.py
   ```

## Mobile Deployment

The mobile deployment files are available in this repository. These files contain all the necessary code for deploying the SafeWayAI application to iOS and Android devices.

### Files Included for Mobile Deployment

- **build_mobile_app.sh**: Script to build the app for both Android and iOS platforms
- **generate_api_keys.py**: Script to guide users through generating the necessary Azure API keys
- **install_safewayai.sh**: Script to help install the APK on Android devices

### Getting Started with Mobile Deployment

1. Build the app:
   ```bash
   ./build_mobile_app.sh
   ```

2. Install on Android:
   ```bash
   ./install_safewayai.sh
   ```

3. For iOS deployment, follow the instructions in the DEPLOYMENT_GUIDE.md file.

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

## Future Enhancements

- Integration with real AI models using camera feeds
- Voice command emergency reporting
- Cloud-based alert syncing and remote admin access
- SMS/Email push notifications
- Enhanced IoT device support
- Expanded insurance partnerships
- Advanced GBV prevention features

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flet framework for the cross-platform UI
- Python community for the excellent libraries
- Microsoft AI For Social Good Hackathon for the inspiration
