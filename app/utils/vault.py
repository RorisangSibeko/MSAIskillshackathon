"""
Secure vault implementation for SafeWayAI application.
This module provides functionality to securely store and retrieve sensitive credentials.
"""

import os
import json
import base64
import logging
import getpass
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

logger = logging.getLogger(__name__)

class SecureVault:
    """Secure vault for storing and retrieving sensitive credentials."""
    
    def __init__(self, vault_file=None, salt_file=None):
        """
        Initialize the secure vault.
        
        Args:
            vault_file (str, optional): Path to the vault file
            salt_file (str, optional): Path to the salt file
        """
        # Set default paths if not provided
        self.vault_file = vault_file or os.path.join(os.path.dirname(__file__), '..', 'config', 'vault.enc')
        self.salt_file = salt_file or os.path.join(os.path.dirname(__file__), '..', 'config', 'salt.bin')
        
        # Ensure directories exist
        os.makedirs(os.path.dirname(self.vault_file), exist_ok=True)
        
        # Initialize vault
        self.vault = {}
        self.key = None
        self.fernet = None
        
        logger.info("Secure vault initialized")
    
    def _derive_key(self, password, salt=None):
        """
        Derive a key from the password and salt.
        
        Args:
            password (str): Password to derive key from
            salt (bytes, optional): Salt to use for key derivation
            
        Returns:
            tuple: (key, salt)
        """
        if salt is None:
            # Generate a new salt if not provided
            salt = os.urandom(16)
        
        # Derive key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        # Derive key from password
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        
        return key, salt
    
    def _save_salt(self, salt):
        """
        Save the salt to a file.
        
        Args:
            salt (bytes): Salt to save
        """
        with open(self.salt_file, 'wb') as f:
            f.write(salt)
    
    def _load_salt(self):
        """
        Load the salt from a file.
        
        Returns:
            bytes: Salt
        """
        if not os.path.exists(self.salt_file):
            return None
        
        with open(self.salt_file, 'rb') as f:
            return f.read()
    
    def unlock(self, password=None):
        """
        Unlock the vault with a password.
        
        Args:
            password (str, optional): Password to unlock the vault
            
        Returns:
            bool: True if vault was unlocked successfully
        """
        try:
            # Get password if not provided
            if password is None:
                password = os.environ.get('SAFEWAYAI_VAULT_PASSWORD')
                
            if password is None:
                password = getpass.getpass("Enter vault password: ")
            
            # Load salt
            salt = self._load_salt()
            
            # Derive key
            key, salt = self._derive_key(password, salt)
            
            # Save salt if it's new
            if not os.path.exists(self.salt_file):
                self._save_salt(salt)
            
            # Create Fernet cipher
            self.key = key
            self.fernet = Fernet(self.key)
            
            # Load vault if it exists
            if os.path.exists(self.vault_file):
                self._load_vault()
            
            logger.info("Vault unlocked successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unlock vault: {e}")
            return False
    
    def _load_vault(self):
        """Load the vault from the vault file."""
        try:
            with open(self.vault_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt the data
            decrypted_data = self.fernet.decrypt(encrypted_data)
            
            # Parse the JSON data
            self.vault = json.loads(decrypted_data.decode())
            
            logger.info("Vault loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load vault: {e}")
            self.vault = {}
    
    def _save_vault(self):
        """Save the vault to the vault file."""
        try:
            # Convert vault to JSON
            data = json.dumps(self.vault).encode()
            
            # Encrypt the data
            encrypted_data = self.fernet.encrypt(data)
            
            # Save to file
            with open(self.vault_file, 'wb') as f:
                f.write(encrypted_data)
            
            logger.info("Vault saved successfully")
            
        except Exception as e:
            logger.error(f"Failed to save vault: {e}")
    
    def set(self, key, value):
        """
        Set a value in the vault.
        
        Args:
            key (str): Key to set
            value (any): Value to set
            
        Returns:
            bool: True if value was set successfully
        """
        try:
            if self.fernet is None:
                logger.error("Vault is locked")
                return False
            
            # Set the value
            self.vault[key] = value
            
            # Save the vault
            self._save_vault()
            
            logger.info(f"Value set for key: {key}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set value: {e}")
            return False
    
    def get(self, key, default=None):
        """
        Get a value from the vault.
        
        Args:
            key (str): Key to get
            default (any, optional): Default value to return if key not found
            
        Returns:
            any: Value from the vault
        """
        try:
            if self.fernet is None:
                logger.error("Vault is locked")
                return default
            
            # Get the value
            return self.vault.get(key, default)
            
        except Exception as e:
            logger.error(f"Failed to get value: {e}")
            return default
    
    def delete(self, key):
        """
        Delete a value from the vault.
        
        Args:
            key (str): Key to delete
            
        Returns:
            bool: True if value was deleted successfully
        """
        try:
            if self.fernet is None:
                logger.error("Vault is locked")
                return False
            
            # Delete the value
            if key in self.vault:
                del self.vault[key]
                
                # Save the vault
                self._save_vault()
                
                logger.info(f"Value deleted for key: {key}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to delete value: {e}")
            return False
    
    def list_keys(self):
        """
        List all keys in the vault.
        
        Returns:
            list: List of keys
        """
        try:
            if self.fernet is None:
                logger.error("Vault is locked")
                return []
            
            # Return list of keys
            return list(self.vault.keys())
            
        except Exception as e:
            logger.error(f"Failed to list keys: {e}")
            return []
    
    def import_config(self, config_dict):
        """
        Import configuration from a dictionary.
        
        Args:
            config_dict (dict): Configuration dictionary
            
        Returns:
            bool: True if configuration was imported successfully
        """
        try:
            if self.fernet is None:
                logger.error("Vault is locked")
                return False
            
            # Import each key-value pair
            for key, value in config_dict.items():
                self.vault[key] = value
            
            # Save the vault
            self._save_vault()
            
            logger.info("Configuration imported successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to import configuration: {e}")
            return False
    
    def export_config(self):
        """
        Export configuration to a dictionary.
        
        Returns:
            dict: Configuration dictionary
        """
        try:
            if self.fernet is None:
                logger.error("Vault is locked")
                return {}
            
            # Return a copy of the vault
            return dict(self.vault)
            
        except Exception as e:
            logger.error(f"Failed to export configuration: {e}")
            return {}
    
    def lock(self):
        """
        Lock the vault.
        
        Returns:
            bool: True if vault was locked successfully
        """
        try:
            # Clear the key and cipher
            self.key = None
            self.fernet = None
            
            # Clear the vault
            self.vault = {}
            
            logger.info("Vault locked successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to lock vault: {e}")
            return False

# Create a singleton instance
vault = SecureVault()
