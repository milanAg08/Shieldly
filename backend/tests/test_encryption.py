# backend/tests/test_encryption.py

import unittest
from backend.ai_backend.security.data_encryption import DataEncryption

class TestEncryption(unittest.TestCase):
    def setUp(self):
        self.encryptor = DataEncryption()
    
    def test_encryption_decryption(self):
        """Test encryption and decryption functionality"""
        original_text = "This is a sensitive piece of information"
        
        # Encrypt the text
        encrypted = self.encryptor.encrypt(original_text)
        
        # Verify encrypted text is different from original
        self.assertNotEqual(original_text, encrypted)
        
        # Decrypt the text
        decrypted = self.encryptor.decrypt(encrypted)
        
        # Verify decryption returns the original text
        self.assertEqual(original_text, decrypted)
    
    def test_empty_text(self):
        """Test encryption and decryption with empty text"""
        original_text = ""
        
        # Encrypt the text
        encrypted = self.encryptor.encrypt(original_text)
        
        # Decrypt the text
        decrypted = self.encryptor.decrypt(encrypted)
        
        # Verify decryption returns the original text
        self.assertEqual(original_text, decrypted)
    
    def test_special_characters(self):
        """Test encryption and decryption with special characters"""
        original_text = "Special characters: !@#$%^&*()_+<>?:{}"
        
        # Encrypt the text
        encrypted = self.encryptor.encrypt(original_text)
        
        # Decrypt the text
        decrypted = self.encryptor.decrypt(encrypted)
        
        # Verify decryption returns the original text
        self.assertEqual(original_text, decrypted)

if __name__ == '__main__':
    unittest.main()