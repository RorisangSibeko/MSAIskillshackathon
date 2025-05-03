import os
import json
import logging
import hashlib
import secrets
from typing import Dict, Optional, List, Any
from datetime import datetime, timedelta
from pathlib import Path

class AuthService:
    """
    Authentication service for SafeWayAI.

    In a production environment, this would use Azure AD B2C or another
    secure authentication service. For the hackathon, we're using a simple
    file-based authentication system.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.current_user = None
        self.users_file = Path("app/data/users.json")
        self.session_token = None
        self.session_expiry = None

        # Ensure the data directory exists
        self.users_file.parent.mkdir(exist_ok=True)

        # Load or create users file
        if not self.users_file.exists():
            self._create_default_users()

    def _create_default_users(self):
        """Create default users for testing."""
        default_users = [
            {
                "username": "admin",
                "password_hash": self._hash_password("admin123"),
                "role": "admin",
                "full_name": "Admin User",
                "email": "admin@safewayai.com",
                "phone": "+1234567890",
                "created_at": datetime.now().isoformat(),
                "subscription_tier": "premium",
                "emergency_contacts": [
                    {"name": "Emergency Contact 1", "phone": "+1987654321", "relationship": "Family"}
                ]
            },
            {
                "username": "responder",
                "password_hash": self._hash_password("respond123"),
                "role": "responder",
                "full_name": "Emergency Responder",
                "email": "responder@safewayai.com",
                "phone": "+1234567891",
                "created_at": datetime.now().isoformat(),
                "subscription_tier": "standard",
                "emergency_contacts": []
            },
            {
                "username": "viewer",
                "password_hash": self._hash_password("view123"),
                "role": "viewer",
                "full_name": "Viewer User",
                "email": "viewer@safewayai.com",
                "phone": "+1234567892",
                "created_at": datetime.now().isoformat(),
                "subscription_tier": "basic",
                "emergency_contacts": []
            }
        ]

        with open(self.users_file, 'w') as f:
            json.dump(default_users, f, indent=2)

        self.logger.info("Created default users file")

    def _hash_password(self, password: str) -> str:
        """Hash a password for storage."""
        # In production, use a proper password hashing library like bcrypt
        return hashlib.sha256(password.encode()).hexdigest()

    def _load_users(self) -> List[Dict[str, Any]]:
        """Load users from the JSON file."""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading users: {e}")
            return []

    def _save_users(self, users: List[Dict[str, Any]]):
        """Save users to the JSON file."""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving users: {e}")

    def login(self, username: str, password: str) -> bool:
        """Authenticate a user with username and password."""
        print(f"Login attempt for user: {username}")

        # Force success for testing
        if username == "admin" and password == "admin123":
            print("FORCING LOGIN SUCCESS FOR ADMIN")
            self.current_user = {
                "username": "admin",
                "role": "admin",
                "full_name": "Admin User",
                "email": "admin@safewayai.com",
                "subscription_tier": "premium"
            }
            self.session_token = secrets.token_hex(16)
            self.session_expiry = datetime.now() + timedelta(hours=24)
            return True

        users = self._load_users()
        print(f"Loaded {len(users)} users")
        print(f"Users: {users}")

        password_hash = self._hash_password(password)
        print(f"Password hash: {password_hash}")

        for i, user in enumerate(users):
            print(f"Checking user {i}: {user.get('username')}")
            if user["username"] == username:
                print(f"Username match found")
                if user["password_hash"] == password_hash:
                    print(f"Password match found - Login successful!")
                    self.current_user = user
                    self.session_token = secrets.token_hex(16)
                    self.session_expiry = datetime.now() + timedelta(hours=24)
                    self.logger.info(f"User {username} logged in")
                    return True
                else:
                    print(f"Password mismatch")
                    print(f"Expected: {user['password_hash']}")
                    print(f"Received: {password_hash}")

        self.logger.warning(f"Failed login attempt for user {username}")
        print(f"Login failed for user: {username}")
        return False

    def logout(self):
        """Log out the current user."""
        self.current_user = None
        self.session_token = None
        self.session_expiry = None
        self.logger.info("User logged out")

    def is_authenticated(self) -> bool:
        """Check if a user is currently authenticated."""
        if not self.current_user or not self.session_token or not self.session_expiry:
            return False

        if datetime.now() > self.session_expiry:
            self.logout()
            return False

        return True

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get the currently authenticated user."""
        if not self.is_authenticated():
            return None

        return self.current_user

    def register_user(self, username: str, password: str, full_name: str,
                      email: str, phone: str, role: str = "viewer") -> bool:
        """Register a new user."""
        users = self._load_users()

        # Check if username already exists
        if any(user["username"] == username for user in users):
            self.logger.warning(f"Registration failed: Username {username} already exists")
            return False

        # Create new user
        new_user = {
            "username": username,
            "password_hash": self._hash_password(password),
            "role": role,
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "created_at": datetime.now().isoformat(),
            "subscription_tier": "basic",
            "emergency_contacts": []
        }

        users.append(new_user)
        self._save_users(users)

        self.logger.info(f"New user registered: {username}")
        return True

    def update_user(self, username: str, updates: Dict[str, Any]) -> bool:
        """Update user information."""
        if not self.is_authenticated():
            return False

        users = self._load_users()

        for i, user in enumerate(users):
            if user["username"] == username:
                # Don't allow updating username or role through this method
                updates.pop("username", None)
                updates.pop("role", None)

                # Hash password if it's being updated
                if "password" in updates:
                    updates["password_hash"] = self._hash_password(updates.pop("password"))

                # Update user
                users[i] = {**user, **updates}
                self._save_users(users)

                # Update current user if this is the logged-in user
                if self.current_user and self.current_user["username"] == username:
                    self.current_user = users[i]

                self.logger.info(f"User {username} updated")
                return True

        return False

    def add_emergency_contact(self, name: str, phone: str, relationship: str) -> bool:
        """Add an emergency contact for the current user."""
        if not self.is_authenticated():
            return False

        username = self.current_user["username"]
        users = self._load_users()

        for i, user in enumerate(users):
            if user["username"] == username:
                contact = {
                    "name": name,
                    "phone": phone,
                    "relationship": relationship
                }

                if "emergency_contacts" not in user:
                    user["emergency_contacts"] = []

                user["emergency_contacts"].append(contact)
                users[i] = user
                self._save_users(users)

                # Update current user
                self.current_user = user

                self.logger.info(f"Emergency contact added for user {username}")
                return True

        return False

    def remove_emergency_contact(self, index: int) -> bool:
        """Remove an emergency contact for the current user."""
        if not self.is_authenticated():
            return False

        username = self.current_user["username"]
        users = self._load_users()

        for i, user in enumerate(users):
            if user["username"] == username:
                if "emergency_contacts" in user and 0 <= index < len(user["emergency_contacts"]):
                    user["emergency_contacts"].pop(index)
                    users[i] = user
                    self._save_users(users)

                    # Update current user
                    self.current_user = user

                    self.logger.info(f"Emergency contact removed for user {username}")
                    return True

        return False

    def get_user_role(self) -> Optional[str]:
        """Get the role of the current user."""
        if not self.is_authenticated():
            return None

        return self.current_user.get("role")

    def get_subscription_tier(self) -> str:
        """Get the subscription tier of the current user."""
        if not self.is_authenticated():
            return "basic"

        return self.current_user.get("subscription_tier", "basic")

    def update_subscription(self, tier: str) -> bool:
        """Update the subscription tier for the current user."""
        if not self.is_authenticated():
            return False

        valid_tiers = ["basic", "standard", "premium", "enterprise"]
        if tier not in valid_tiers:
            return False

        return self.update_user(self.current_user["username"], {"subscription_tier": tier})
