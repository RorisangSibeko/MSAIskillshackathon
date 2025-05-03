#!/usr/bin/env python3
"""
Test script for the secure vault implementation.
This script tests the vault functionality by storing and retrieving a test value.
"""

import os
import sys
import getpass
from pathlib import Path

# Add the parent directory to the path so we can import the app modules
sys.path.insert(0, str(Path(__file__).parent))

from app.utils.vault import vault

def main():
    """Main function to test the vault."""
    print("=" * 80)
    print("SafeWayAI Vault Test".center(80))
    print("=" * 80)
    print("\nThis script tests the secure vault implementation.\n")
    
    # Get the vault password
    password = getpass.getpass("Enter the vault password: ")
    
    # Unlock the vault with the password
    if not vault.unlock(password):
        print("\nError: Failed to unlock the vault.")
        return 1
    
    # Test storing a value
    test_key = "TEST_KEY"
    test_value = "This is a test value"
    
    print(f"\nStoring test value: {test_key} = {test_value}")
    if not vault.set(test_key, test_value):
        print("\nError: Failed to store test value.")
        return 1
    
    # Test retrieving the value
    retrieved_value = vault.get(test_key)
    print(f"\nRetrieved test value: {test_key} = {retrieved_value}")
    
    if retrieved_value != test_value:
        print("\nError: Retrieved value does not match stored value.")
        return 1
    
    # List all keys in the vault
    keys = vault.list_keys()
    print("\nAll keys in the vault:")
    for key in keys:
        print(f"- {key}")
    
    # Lock the vault
    vault.lock()
    print("\nVault locked.")
    
    print("\nVault test completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
