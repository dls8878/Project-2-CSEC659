import unittest
from projecttwo import generate_password, encrypt_data, decrypt_data, load_key
import string

class TestPasswordManager(unittest.TestCase):
    def test_generate_password_length(self):
        """Test if the generated password meets the requested length."""
        length = 12
        password = generate_password(length, include_special_chars=False)
        self.assertEqual(len(password), length)

    def test_generate_password_special_chars(self):
        """Test if the generated password includes special characters when requested."""
        password = generate_password(12, True)
        has_special = any(char in string.punctuation for char in password)
        self.assertTrue(has_special)

    def test_encryption_decryption(self):
        """Test if data is correctly encrypted and decrypted using the same key."""
        key = load_key()  # Assuming this function gets the current encryption key
        original_data = "Test data for encryption"
        encrypted_data = encrypt_data(original_data, key)
        decrypted_data = decrypt_data(encrypted_data, key)
        self.assertEqual(original_data, decrypted_data)



if __name__ == '__main__':
    unittest.main()
