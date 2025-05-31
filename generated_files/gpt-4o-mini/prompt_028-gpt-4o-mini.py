import argparse
import os
from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key(password):
    # Generate a key from the password
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def encrypt_file(file_path, password):
    key = generate_key(password)
    fernet = Fernet(key)

    with open(file_path, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(file_path + '.encrypted', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

    print(f"File encrypted and saved as {file_path}.encrypted")

def decrypt_file(file_path, password):
    key = generate_key(password)
    fernet = Fernet(key)

    with open(file_path, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = fernet.decrypt(encrypted)

    decrypted_file_path = file_path.replace('.encrypted', '')
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted)

    print(f"File decrypted and saved as {decrypted_file_path}")

def main():
    parser = argparse.ArgumentParser(description='Encrypt or Decrypt a file.')
    parser.add_argument('action', choices=['encrypt', 'decrypt'], help='Action to perform on the file')
    parser.add_argument('file_path', help='Path to the file')
    parser.add_argument('password', help='Password for encryption/decryption')

    args = parser.parse_args()

    if not os.path.isfile(args.file_path):
        print("File does not exist.")
        return

    if args.action == 'encrypt':
        encrypt_file(args.file_path, args.password)
    elif args.action == 'decrypt':
        if not args.file_path.endswith('.encrypted'):
            print("Invalid file for decryption. It should have .encrypted extension")
            return
        decrypt_file(args.file_path, args.password)

if __name__ == "__main__":
    main()