## Emoji Encrypt 🔒🤖
#### PythonLicense

A secure, command-line encryption tool that transforms your plain text messages into strings of emojis. Unlike simple substitution ciphers, emoji-encrypt uses a cryptographically secure stream cipher, ensuring your messages are not just fun to look at, but safe to share.

Perfect for hiding messages in plain sight or sending secrets that only look like gibberish.

*Features* 🌟
🔐 Secure Encryption: Uses SHA-256 hashing combined with an XOR stream cipher to protect your data.
🔄 UTF-8 Support: Encrypts any text, including special characters, symbols, and even other emojis.
🛡️ Robust Decoding: Automatically handles "invisible" Unicode characters (like variation selectors) to prevent copy-paste errors.
🎲 Dynamic Mapping: Generates a unique emoji table based on your password.
⚡ Zero Dependencies: Runs on standard Python libraries—no pip install required!
How It Works 🧠
Password Hashing: Your password is hashed using SHA-256 to create a secure seed.
Keystream Generation: A unique pseudo-random byte stream is generated based on the seed.
XOR Encryption: Your text is XORed with the keystream.
Emoji Mapping: The resulting bytes are mapped to a dynamically generated set of atomic emojis.
Installation 🛠️
Prerequisites
Python 3.6 or higher.
Setup
Clone the repository and navigate into the directory:

```
git clone https://github.com/your-username/emoji-encrypt.gitcd emoji-encrypt
```
*Usage* 📝
Run the script using Python:

```
bash

python3 emoji_encrypt.py
```
Follow the interactive prompts:

Enter a password: Create a strong password. You will need this exact password to decrypt the message later!
Choose Action: Type encrypt or decrypt.
Input Text: Paste your text or the emoji sequence.
Example
Encryption:

text

Enter password: super_secret_pass
Choose action (encrypt/decrypt): encrypt
Enter text to encrypt: Hello World!

Encrypted Emoji Stream:
🙃🧝🤯👩‍🎤🤨👁️‍🗨️⛷️😵💆‍♀️🤸‍♂️👁️‍🗨️
Decryption:

text

Enter password: super_secret_pass
Choose action (encrypt/decrypt): decrypt
Enter emoji sequence to decrypt: 🙃🧝🤯👩‍🎤🤨👁️‍🗨️⛷️😵💆‍♀️🤸‍♂️👁️‍🗨️

Decrypted Text:
Hello World!
⚠️ Note: Due to dynamic emoji generation, ensure you are using the same version of the script to decrypt that you used to encrypt.

Author 🧑‍💻
[https://t.me/ROCKMURPHY]

Made with somethink akin to love and Python.
