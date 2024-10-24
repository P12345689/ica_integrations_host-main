#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from cryptography.fernet import Fernet

# Replace 'your_key_here' with your actual Fernet key
key = ""
fernet = Fernet(key)

# Test data
text = ""

# Encrypt
encrypted = fernet.encrypt(text.encode())
print("Encrypted:", encrypted.decode())

encrypted = ""
# Decrypt
try:
    decrypted = fernet.decrypt(encrypted).decode()
    print("Decrypted:", decrypted)
except Exception as e:
    print("Decryption failed:", str(e))
