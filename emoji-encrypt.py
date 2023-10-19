import random
import string

def generate_emoji_mapping(seed, characters, emojis):
    """
    Generate a random emoji-character mapping based on a seed.
    """
    random.seed(seed)
    shuffled_emojis = random.sample(emojis, len(emojis))
    return dict(zip(characters, shuffled_emojis))

def emoji_encrypt(text, mapping):
    """Encrypt a text using the given emoji-character mapping."""
    encrypted_text = ''.join([mapping.get(char, char) for char in text])
    return encrypted_text

def emoji_decrypt(emoji_text, mapping):
    """Decrypt an emoji text using the given emoji-character mapping."""
    reverse_mapping = {v: k for k, v in mapping.items()}
    decrypted_text = ''.join([reverse_mapping.get(emoji, emoji) for emoji in emoji_text])
    return decrypted_text

if __name__ == "__main__":
    # Define a set of characters for our mapping
    characters = string.ascii_letters + string.digits + string.punctuation + string.whitespace
    
    # A larger set of emojis (more can be added as needed)
    emojis = [
    '🍎', '🍌', '🍇', '🍉', '🍋', '🍍', '🍒', '🍓', '🥥', '🥝',
    '🍏', '🍊', '🍐', '🍑', '🍈', '🍖', '🍗', '🥩', '🥓', '🍔',
    '🍟', '🍕', '🌭', '🍿', '🥪', '🥙', '🍤', '🍣', '🍥', '🍦',
    '🍧', '🍨', '🍩', '🍪', '🎂', '🍰', '🧁', '🥧', '🍫', '🍬',
    '🍭', '🍮', '🍯', '🍼', '🥛', '🍵', '🍶', '🍷', '🍸', '🍹',
    '🍺', '🍻', '🥂', '🥃', '🥄', '🍴', '🍽', '🥢', '🧂', '🥤',
    '🍼', '🥤', '🥢', '🍴', '🍽', '🍾', '🍷', '🍸', '🍹', '🍺',
    '🍻', '🥂', '🥃', '🍽', '🍴', '🍵', '🥛', '🍼', '🍺', '🍻',
    '🥂', '🥃', '🍷', '🍸', '🍹', '🍺', '🍻', '🥂', '🥃', '🍽',
    '🍴', '🍵', '🥛', '🍼', '🍾', '🍷', '🍸', '🍹', '🍺', '🍻'
    ]
    
    seed = input("Enter a seed: ")
    random_emoji_mapping = generate_emoji_mapping(seed, characters, emojis)
    
    action = input("Choose action (encrypt/decrypt): ").lower()
    if action == "encrypt":
        plaintext = input("Enter the text to encrypt: ")
        encrypted_text = emoji_encrypt(plaintext, random_emoji_mapping)
        print(f"Encrypted Text: {encrypted_text}")
    elif action == "decrypt":
        emoji_sequence = input("Enter the emoji sequence to decrypt: ")
        decrypted_text = emoji_decrypt(emoji_sequence, random_emoji_mapping)
        print(f"Decrypted Text: {decrypted_text}")
    else:
        print("Invalid action.")
