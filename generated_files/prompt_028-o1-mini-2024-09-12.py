import argparse
import os
import sys
from getpass import getpass
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import secrets

def derive_key(password: str, salt: bytes, algorithm: str) -> bytes:
    if algorithm == 'AES':
        key_length = 32  # AES-256
    else:
        raise ValueError("Unsupported algorithm")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=key_length,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(input_path: str, output_path: str, password: str, algorithm: str):
    with open(input_path, 'rb') as f:
        data = f.read()
    salt = secrets.token_bytes(16)
    key = derive_key(password, salt, algorithm)
    if algorithm == 'AES':
        iv = secrets.token_bytes(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    else:
        raise ValueError("Unsupported algorithm")
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    with open(output_path, 'wb') as f:
        f.write(salt + iv + ciphertext)

def decrypt_file(input_path: str, output_path: str, password: str, algorithm: str):
    with open(input_path, 'rb') as f:
        data = f.read()
    salt = data[:16]
    if algorithm == 'AES':
        iv = data[16:32]
        ciphertext = data[32:]
        key = derive_key(password, salt, algorithm)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=defaultbackend())
    else:
        raise ValueError("Unsupported algorithm")
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    try:
        plaintext = unpadder.update(padded_data) + unpadder.finalize()
    except ValueError:
        print("Incorrect password or corrupted file.")
        sys.exit(1)
    with open(output_path, 'wb') as f:
        f.write(plaintext)

def main():
    parser = argparse.ArgumentParser(description='Encrypt or decrypt files.')
    parser.add_argument('mode', choices=['encrypt', 'decrypt'], help='Mode: encrypt or decrypt')
    parser.add_argument('-i', '--input', required=True, help='Input file path')
    parser.add_argument('-o', '--output', required=True, help='Output file path')
    parser.add_argument('-a', '--algorithm', choices=['AES'], default='AES', help='Encryption algorithm')
    parser.add_argument('-p', '--password', help='Password (will prompt if not provided)')
    args = parser.parse_args()

    if args.password:
        password = args.password
    else:
        password = getpass("Enter password: ")

    if args.mode == 'encrypt':
        encrypt_file(args.input, args.output, password, args.algorithm)
        print(f"File encrypted and saved to {args.output}")
    else:
        decrypt_file(args.input, args.output, password, args.algorithm)
        print(f"File decrypted and saved to {args.output}")

if __name__ == '__main__':
    main()