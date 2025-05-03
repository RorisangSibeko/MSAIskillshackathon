#!/usr/bin/env python3
"""
SafeWayAI Vault Initializer

This script initializes the secure vault with Azure credentials.
It should be run once during setup to securely store the credentials.
"""

import os
import sys
import getpass
import logging
from pathlib import Path

# Add the parent directory to the path so we can import the app modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.utils.vault import vault
from app.config.azure_config import initialize_vault_with_real_values

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main function to initialize the vault."""
    print("=" * 80)
    print("SafeWayAI Vault Initializer".center(80))
    print("=" * 80)
    print("\nThis script will initialize the secure vault with Azure credentials.\n")
    
    # Get the vault password
    password = getpass.getpass("Enter a secure password for the vault: ")
    confirm_password = getpass.getpass("Confirm password: ")
    
    if password != confirm_password:
        print("\nError: Passwords do not match.")
        return 1
    
    # Unlock the vault with the password
    if not vault.unlock(password):
        print("\nError: Failed to unlock the vault.")
        return 1
    
    # Initialize the vault with real values
    if not initialize_vault_with_real_values():
        print("\nError: Failed to initialize the vault with real values.")
        return 1
    
    # Save the password to an environment variable file for development
    env_dir = Path(__file__).parent.parent / "assets"
    env_dir.mkdir(exist_ok=True)
    
    env_file = env_dir / ".env"
    
    # Check if .env file exists
    if env_file.exists():
        # Read existing content
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Check if SAFEWAYAI_VAULT_PASSWORD is already set
        if "SAFEWAYAI_VAULT_PASSWORD" in content:
            # Update the password
            lines = content.splitlines()
            new_lines = []
            for line in lines:
                if line.startswith("SAFEWAYAI_VAULT_PASSWORD="):
                    new_lines.append(f"SAFEWAYAI_VAULT_PASSWORD={password}")
                else:
                    new_lines.append(line)
            
            # Write the updated content
            with open(env_file, 'w') as f:
                f.write("\n".join(new_lines))
        else:
            # Append the password
            with open(env_file, 'a') as f:
                f.write(f"\nSAFEWAYAI_VAULT_PASSWORD={password}")
    else:
        # Create a new .env file
        with open(env_file, 'w') as f:
            f.write(f"SAFEWAYAI_VAULT_PASSWORD={password}")
    
    print("\nVault initialized successfully!")
    print(f"The vault password has been saved to {env_file}")
    print("You can now run the application with secure credentials.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
