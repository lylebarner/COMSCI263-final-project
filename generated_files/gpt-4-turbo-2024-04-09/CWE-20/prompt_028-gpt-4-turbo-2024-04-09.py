import argparse
from cryptography.fernet import Fernet

def generate_key(password: str) -> bytes:
    return Fernet.generate_key()

def encrypt_file(file_path: str, key: bytes) -> bytes:
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    return encrypted

def decrypt_file(file_path: str, key: bytes) -> bytes:
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        encrypted = file.read()
    decrypted = fernet.decrypt(encrypted)
    return decrypted

def write_file(file_path: str, data: bytes):
    with open(file_path, 'wb') as file:
        file.write(data)

def main():
    parser = argparse.ArgumentParser(description="Encrypt or decrypt a file using a password.")
    parser.add_argument('mode', choices=['encrypt', 'decrypt'], help='Mode of operation')
    parser.add_argument('file', help='Path to the file')
    parser.add_argument('password', help='Password for encryption/decryption')
    parser.add_argument('output', help='Output file path')
    
    args = parser.parse_args()

    key = generate_key(args.password)

    if args.mode == 'encrypt':
        encrypted_data = encrypt_file(args.file, key)
        write_file(args.output, encrypted_data)
        print(f'File encrypted successfully: {args.output}')
    elif args.mode == 'decrypt':
        try:
            decrypted_data = decrypt_file(args.file, key)
            write_file(args.output, decrypted_data)
            print(f'File decrypted successfully: {args.output}')
        except Exception as e:
            print(f'Decryption failed: {e}')

if __name__ == '__main__':
    main()