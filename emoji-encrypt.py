import hashlib
import random
import string
from typing import List, Dict

class SecureEmojiCipher:
   # Stream Crypter!

    def __init__(self, password: str):
        # Password!
        if not password:
            raise ValueError("Password cannot be empty.")

        # Generate a numeric seed from the password using SHA-256
        self.password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.seed_int = int(self.password_hash, 16)
        
        # Create the Emoji Map (0-255)
        all_emojis = self._get_emoji_database()
        if len(all_emojis) < 256:
            raise RuntimeError("Emoji database is too small. Need at least 256 unique emojis.")
        
        # Create a deterministic RNG based on the password
        rng = random.Random(self.seed_int)
        
        # Shuffle the emojis to create a random substitution table for the bytes 0-255
        self.emoji_table = rng.sample(all_emojis, 256)
        
        # Create reverse lookup: Emoji -> Byte Index (for decryption)
        self.reverse_emoji_table = {emoji: i for i, emoji in enumerate(self.emoji_table)}

    def _get_keystream_byte(self, index: int) -> int:
        # Generates a cryptographic pseudo-random byte for a specific index.
       
        # Combine the master hash with the current index to get a unique hash
        data_to_hash = f"{self.password_hash}{index}".encode('utf-8')
        # Return the first byte of the SHA256 hash
        return hashlib.sha256(data_to_hash).digest()[0]

    def encrypt(self, plaintext: str) -> str:
        # Encrypts text by XORing bytes with a keystream and mapping to emojis.
        # Convert text to raw bytes (handles UTF-8, special chars, etc.)
        plain_bytes = plaintext.encode('utf-8')
        encrypted_chars = []

        for i, byte_val in enumerate(plain_bytes):
            # Get keystream byte
            key_byte = self._get_keystream_byte(i)
            
            # XOR (The encryption operation)
            encrypted_byte = byte_val ^ key_byte
            
            # Map resulting byte (0-255) to an emoji
            encrypted_chars.append(self.emoji_table[encrypted_byte])
            
        return ''.join(encrypted_chars)

    def decrypt(self, ciphertext: str) -> str:
        # It is safer to iterate strictly over the string indices to handle 
        decrypted_bytes = []
        
        # We need to iterate through the string finding our specific emojis.
        current_index = 0
        
        # Create a fast lookup map for scanning if needed, 
        # but since we have a direct map in reverse_emoji_table:
        
        # NOTE: Standard iteration over a string in Python splits by Unicode code point.
        
        for i, char in enumerate(ciphertext):
            if char in self.reverse_emoji_table:
                # Map emoji back to encrypted byte value
                encrypted_byte = self.reverse_emoji_table[char]
                
                # Recreate keystream byte
                key_byte = self._get_keystream_byte(i)
                
                # XOR to retrieve original byte
                decrypted_byte = encrypted_byte ^ key_byte
                decrypted_bytes.append(decrypted_byte)
            else:
                # If we encounter an emoji not in our map (e.g. from a different version),
                # we can't decrypt it properly. We raise an error or skip.
                # Here we raise to ensure integrity.
                raise ValueError(f"Invalid emoji found at position {i}: {char}. Cannot decrypt.")

        # Convert bytes back to string
        return bytes(decrypted_bytes).decode('utf-8')

    @staticmethod
    def _get_emoji_database() -> List[str]:
        # A curated list of diverse emojis to ensure we hit 256+
        raw_list = [
            '😀','😃','😄','😁','😆','😅','🤣','😂','🙂','🙃','😉','😊','😇','🥰','😍','🤩','😘','😗','😚','😙',
            '😋','😛','😜','🤪','😝','🤑','🤗','🤭','🤫','🤔','🤐','🤨','😐','😑','😶','😏','😒','🙄','😬','🤥',
            '😌','😔','😪','🤤','😴','😷','🤒','🤕','🤢','🤮','🤧','🥵','🥶','🥴','😵','🤯','🤠','🥳','😎','🤓',
            '🧐','😕','😟','🙁','☹️','😮','😯','😲','😳','🥺','😦','😧','😨','😰','😥','😢','😭','😱','😖','😣',
            '😞','😓','😩','😫','🥱','😤','😡','😠','🤬','😈','👿','💀','☠️','💩','🤡','👹','👺','👻','👽','👾',
            '🤖','😺','😸','😹','😻','😼','😽','🙀','😿','😾','🙈','🙉','🙊','💋','💌','💘','💝','💖','💗','💓',
            '💞','💕','💟','❣️','💔','❤️','🧡','💛','💚','💙','💜','🤎','🖤','🤍','💯','💢','💥','💫','💦','💨',
            '🕳️','💣','💬','👁️‍🗨️','🗨️','🗯️','💭','💤','👋','🤚','🖐️','✋','🖖','👌','🤏','✌️','🤞','🤟','🤘','🤙',
            '👈','👉','👆','🖕','👇','☝️','👍','👎','✊','👊','🤛','🤜','👏','🙌','👐','🤲','🤝','🙏','✍️','💅',
            '🤳','💪','🦾','🦿','🦵','🦶','👂','🦻','👃','🧠','🫀','🫁','🦷','🦴','👀','👁️','👅','👄','👶','🧒',
            '👦','👧','🧑','👱','👨','🧔','👩','🧓','👴','👵','🙍','🙎','🙅','🙆','💁','🙋','🧏','🙇','🤦','🤷',
            '👨‍⚕️','👩‍⚕️','👨‍🎓','👩‍🎓','👨‍🏫','👩‍🏫','👨‍⚖️','👩‍⚖️','👨‍🌾','👩‍🌾','👨‍🍳','👩‍🍳','👨‍🔧','👩‍🔧','👨‍🏭','👩‍🏭',
            '👨‍💼','👩‍💼','👨‍🔬','👩‍🔬','👨‍💻','👩‍💻','👨‍🎤','👩‍🎤','👨‍🎨','👩‍🎨','👨‍✈️','👩‍✈️','👨‍🚀','👩‍🚀','👨‍🚒','👩‍🚒',
            '👮','🕵️','💂','👷','🤴','👸','👳','👲','🧕','🤵','👰','🤰','🤱','👼','🎅','🤶','🦸','🦹','🧙','🧚',
            '🧛','🧜','🧝','🧞','🧟','💆','💇','🚶','🧍','🧎','🧑‍🦯','🧑‍🦼','🧑‍🦽','🏃','💃','🕺','🕴️','👯','🧖','🧘',
            '🧗','🤺','🏇','⛷️','🏂','🏌️','🏄','🚣','🏊','⛹️','🏋️','🚴','🚵','🤸','🤼','🤽','🤾','🤹','🛀','🛌'
        ]
        # Deduplicate just in case
        return list(set(raw_list))

def main():
    print("--- Secure Emoji Encryption (Stream Cipher) ---")
    
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
                print("Ensure you are using the exact same password and that no emojis were modified.")
                
        else:
            print("Invalid action.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
