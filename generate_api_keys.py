#!/usr/bin/env python3
"""
SafeWayAI API Key Generator

This script helps you generate and configure the necessary API keys for the SafeWayAI application.
It will guide you through the process of creating the required Azure resources and configuring
the app to use them.
"""

import os
import sys
import json
import getpass
import webbrowser
from pathlib import Path

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the script header."""
    clear_screen()
    print("=" * 80)
    print("SafeWayAI API Key Generator".center(80))
    print("=" * 80)
    print("\nThis script will help you generate and configure the necessary API keys for SafeWayAI.\n")

def open_azure_portal():
    """Open the Azure Portal in a web browser."""
    print("Opening Azure Portal in your web browser...")
    webbrowser.open("https://portal.azure.com/")
    input("\nPress Enter once you've logged in to the Azure Portal...")

def create_resource_group():
    """Guide the user to create an Azure resource group."""
    print("\n--- Step 1: Create a Resource Group ---\n")
    print("In the Azure Portal:")
    print("1. Click on 'Resource groups' in the left sidebar")
    print("2. Click '+ Create' to create a new resource group")
    print("3. Enter 'SafeWayAI-Resources' as the name")
    print("4. Select your preferred region")
    print("5. Click 'Review + create', then 'Create'")
    
    input("\nPress Enter once you've created the resource group...")

def create_cosmos_db():
    """Guide the user to create an Azure Cosmos DB account."""
    print("\n--- Step 2: Create a Cosmos DB Account ---\n")
    print("In the Azure Portal:")
    print("1. Search for 'Cosmos DB' in the search bar")
    print("2. Click 'Create' to create a new Cosmos DB account")
    print("3. Select 'Core (SQL)' as the API")
    print("4. Enter 'safewayai-db' as the account name")
    print("5. Select the 'SafeWayAI-Resources' resource group")
    print("6. Select your preferred region")
    print("7. Click 'Review + create', then 'Create'")
    print("8. Wait for the deployment to complete")
    print("9. Go to the 'Keys' section and copy the PRIMARY CONNECTION STRING")
    
    cosmos_key = getpass.getpass("\nEnter your Cosmos DB Connection String: ")
    return cosmos_key

def create_maps_account():
    """Guide the user to create an Azure Maps account."""
    print("\n--- Step 3: Create an Azure Maps Account ---\n")
    print("In the Azure Portal:")
    print("1. Search for 'Maps' in the search bar")
    print("2. Click 'Create' to create a new Maps account")
    print("3. Enter 'safewayai-maps' as the name")
    print("4. Select the 'SafeWayAI-Resources' resource group")
    print("5. Select 'S1' as the pricing tier")
    print("6. Click 'Review + create', then 'Create'")
    print("7. Wait for the deployment to complete")
    print("8. Go to the 'Authentication' section and copy the PRIMARY KEY")
    
    maps_key = getpass.getpass("\nEnter your Azure Maps Primary Key: ")
    return maps_key

def create_cognitive_services():
    """Guide the user to create Azure Cognitive Services."""
    print("\n--- Step 4: Create Azure Cognitive Services ---\n")
    print("In the Azure Portal:")
    print("1. Search for 'Cognitive Services' in the search bar")
    print("2. Click 'Create' to create a new Cognitive Services resource")
    print("3. Select 'Language Service' as the type")
    print("4. Enter 'safewayai-language' as the name")
    print("5. Select the 'SafeWayAI-Resources' resource group")
    print("6. Select your preferred region")
    print("7. Select 'S0' as the pricing tier")
    print("8. Click 'Review + create', then 'Create'")
    print("9. Wait for the deployment to complete")
    print("10. Go to the 'Keys and Endpoint' section and copy KEY 1")
    
    cognitive_key = getpass.getpass("\nEnter your Cognitive Services Key: ")
    cognitive_endpoint = input("Enter your Cognitive Services Endpoint: ")
    return cognitive_key, cognitive_endpoint

def save_config(cosmos_key, maps_key, cognitive_key, cognitive_endpoint):
    """Save the API keys to a configuration file."""
    config = {
        "COSMOS_DB_CONNECTION_STRING": cosmos_key,
        "AZURE_MAPS_KEY": maps_key,
        "AZURE_COGNITIVE_KEY": cognitive_key,
        "AZURE_COGNITIVE_ENDPOINT": cognitive_endpoint
    }
    
    # Create the .env file
    env_content = "\n".join([f"{k}={v}" for k, v in config.items()])
    
    # Save to assets directory
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)
    
    with open(assets_dir / ".env", "w") as f:
        f.write(env_content)
    
    print("\n--- Configuration Saved ---\n")
    print(f"API keys have been saved to {assets_dir / '.env'}")
    print("This file will be included in the mobile app build.")

def main():
    """Main function to run the script."""
    print_header()
    
    # Check if the user wants to proceed
    proceed = input("Do you want to proceed with generating API keys? (y/n): ")
    if proceed.lower() != 'y':
        print("\nExiting the script. You can run it again later.")
        sys.exit(0)
    
    # Guide the user through the process
    open_azure_portal()
    create_resource_group()
    cosmos_key = create_cosmos_db()
    maps_key = create_maps_account()
    cognitive_key, cognitive_endpoint = create_cognitive_services()
    
    # Save the configuration
    save_config(cosmos_key, maps_key, cognitive_key, cognitive_endpoint)
    
    print("\n--- All Done! ---\n")
    print("You have successfully generated and configured the API keys for SafeWayAI.")
    print("You can now build the mobile app with these keys.")
    print("\nThank you for using SafeWayAI!")

if __name__ == "__main__":
    main()
