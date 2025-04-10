# backend/ai_backend/security/data_encryption.py

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class DataEncryption:
    """Handles encryption and decryption of sensitive user data"""
    
    def __init__(self, secret_key=None):
        """Initialize encryption with a secret key or generate one"""
        if secret_key:
            self.secret_key = secret_key
        else:
            # Use the application's secret key or generate a new one
            self.secret_key = os.environ.get('SECRET_KEY', os.urandom(32))
        
        # Generate a key from the secret key
        self.key = self._generate_key(self.secret_key)
        self.cipher = Fernet(self.key)
    
    def _generate_key(self, secret_key):
        """Generate a Fernet key from a secret key"""
        if isinstance(secret_key, str):
            secret_key = secret_key.encode()
        
        # Use PBKDF2 to derive a key from the secret key
        salt = b'shieldly_static_salt'  # In production, use a secure, unique salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        key = base64.urlsafe_b64encode(kdf.derive(secret_key))
        return key
    
    def encrypt(self, data):
        """
        Encrypt string data
        
        Args:
            data (str): The data to encrypt
            
        Returns:
            str: Encrypted data as a base64 string
        """
        if not data:
            return None
            
        if isinstance(data, str):
            data = data.encode()
            
        encrypted_data = self.cipher.encrypt(data)
        return encrypted_data.decode()
    
    def decrypt(self, encrypted_data):
        """
        Decrypt encrypted data
        
        Args:
            encrypted_data (str): The encrypted data as a base64 string
            
        Returns:
            str: Decrypted data
        """
        if not encrypted_data:
            return None
            
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()
            
        try:
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return decrypted_data.decode()
        except Exception as e:
            # Log error in production
            print(f"Decryption error: {e}")
            return None