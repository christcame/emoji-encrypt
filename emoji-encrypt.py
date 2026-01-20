import hashlib
import random
import re
import unicodedata
from typing import List, Dict

class SecureEmojiCipher:
    # Stream Cypher!

    def __init__(self, password: str):
        if not password:
            raise ValueError("Password cannot be empty.")

        # Generate Seed from Password
        self.password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.seed_int = int(self.password_hash, 16)
        
        # Dynamically generate a clean list of emojis
        clean_emojis = self._generate_atomic_emojis()
        
        if len(clean_emojis) < 256:
            raise RuntimeError(f"System error: Generated only {len(clean_emojis)} emojis. Need 256.")
        
        # Create the Mapping (0-255)
        rng = random.Random(self.seed_int)
        self.emoji_table = rng.sample(clean_emojis, 256)
        self.reverse_emoji_table = {emoji: i for i, emoji in enumerate(self.emoji_table)}

    def _generate_atomic_emojis(self) -> List[str]:
        # Generates a list of emojis by iterating through Unicode ranges.
        emojis = []
        
        # Emoticons (Classic faces) - U+1F600 to U+1F64F
        for code in range(0x1F600, 0x1F650):
            emojis.append(chr(code))
            
        # Transport & Map Symbols - U+1F680 to U+1F6FF
        for code in range(0x1F680, 0x1F700):
            emojis.append(chr(code))
            
        # Misc Symbols and Pictographs - U+1F300 to U+1F5FF (Subset)
        # We skip some ranges that might contain multi-char combos
        for code in range(0x1F300, 0x1F400): 
            emojis.append(chr(code))

        # Geometric Shapes Extended - U+1F780 to U+1F7FF
        for code in range(0x1F780, 0x1F7F0):
            emojis.append(chr(code))
            
        # Supplemental Symbols and Pictographs - U+1F900 to U+1F9FF
        for code in range(0x1F900, 0x1F9B0):
            emojis.append(chr(code))

        return emojis

    def _get_keystream_byte(self, index: int) -> int:
        data_to_hash = f"{self.password_hash}{index}".encode('utf-8')
        return hashlib.sha256(data_to_hash).digest()[0]

    def encrypt(self, plaintext: str) -> str:
        plain_bytes = plaintext.encode('utf-8')
        encrypted_chars = []
        for i, byte_val in enumerate(plain_bytes):
            key_byte = self._get_keystream_byte(i)
            encrypted_byte = byte_val ^ key_byte
            encrypted_chars.append(self.emoji_table[encrypted_byte])
        return ''.join(encrypted_chars)

    def decrypt(self, ciphertext: str) -> str:
        # Normalize input to remove variation selectors
        cleaned_text = unicodedata.normalize('NFC', ciphertext)
        cleaned_text = re.sub(r'[\ufe0e\ufe0f]', '', cleaned_text)
        
        decrypted_bytes = []
        for i, char in enumerate(cleaned_text):
            if char in self.reverse_emoji_table:
                encrypted_byte = self.reverse_emoji_table[char]
                key_byte = self._get_keystream_byte(i)
                decrypted_bytes.append(encrypted_byte ^ key_byte)
            else:
                # If this happens, the text was encrypted with a different database version
                raise ValueError(
                    f"Character mismatch at position {i}: '{char}'. "
                    "This text was likely encrypted with a different version of the tool. "
                    "Please re-encrypt your text with this version."
                )
        return bytes(decrypted_bytes).decode('utf-8')

def main():
    print("--- Stable Secure Emoji Encryption ---")
    print("NOTE: This version uses a dynamically generated emoji list.")
    print("Text encrypted with older versions cannot be decrypted here.\n")
    
    try:
        password = input("Enter password: ")
        if not password:
            print("Password required.")
            return

        cipher = SecureEmojiCipher(password)
        
        action = input("Choose action (encrypt/decrypt): ").strip().lower()
        
        if action == "encrypt":
            text = input("Enter text to encrypt: ")
            result = cipher.encrypt(text)
            print(f"\nEncrypted Emoji Stream:\n{result}")
            
        elif action == "decrypt":
            text = input("Enter emoji sequence to decrypt: ")
            try:
                result = cipher.decrypt(text)
                print(f"\nDecrypted Text:\n{result}")
            except ValueError as e:
                print(f"\nDecryption Failed: {e}")
                
        else:
            print("Invalid action.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
