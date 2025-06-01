import argparse
import getpass
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidTag
import base64
import secrets

SUPPORTED_ALGOS = {
    'aes-256-gcm': {
        'key_len': 32,
        'nonce_len': 12,
    },
    'aes-128-cbc': {
        'key_len': 16,
        'iv_len': 16,
    }
}

def derive_key(password, salt, length):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        iterations=200000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(filepath, password, algorithm):
    config = SUPPORTED_ALGOS[algorithm]
    salt = secrets.token_bytes(16)
    key = derive_key(password, salt, config['key_len'])

    with open(filepath, 'rb') as f:
        data = f.read()

    if algorithm == 'aes-256-gcm':
        nonce = secrets.token_bytes(config['nonce_len'])
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        ct = encryptor.update(data) + encryptor.finalize()
        tag = encryptor.tag
        out_data = b'ALG:' + algorithm.encode() + b'|SALT:' + base64.b64encode(salt) + b'|NONCE:' + base64.b64encode(nonce) + b'|TAG:' + base64.b64encode(tag) + b'|DATA:' + base64.b64encode(ct)
    elif algorithm == 'aes-128-cbc':
        iv = secrets.token_bytes(config['iv_len'])
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        # PKCS7 padding
        pad_len = 16 - (len(data) % 16)
        data += bytes([pad_len]) * pad_len
        ct = encryptor.update(data) + encryptor.finalize()
        out_data = b'ALG:' + algorithm.encode() + b'|SALT:' + base64.b64encode(salt) + b'|IV:' + base64.b64encode(iv) + b'|DATA:' + base64.b64encode(ct)
    else:
        raise ValueError('Unsupported algorithm')

    outpath = filepath + '.enc'
    with open(outpath, 'wb') as outf:
        outf.write(out_data)
    print(f'File encrypted to {outpath}')

def decrypt_file(filepath, password):
    with open(filepath, 'rb') as f:
        content = f.read()

    # Parse metadata
    try:
        meta, bdata = content.split(b'|DATA:', 1)
        meta_parts = dict(
            part.split(b':', 1) for part in meta.split(b'|')
        )
        algorithm = meta_parts[b'ALG'].decode()
        salt = base64.b64decode(meta_parts[b'SALT'])
        if algorithm == 'aes-256-gcm':
            nonce = base64.b64decode(meta_parts[b'NONCE'])
            tag = base64.b64decode(meta_parts[b'TAG'])
        elif algorithm == 'aes-128-cbc':
            iv = base64.b64decode(meta_parts[b'IV'])
        else:
            print(f"Unsupported algorithm in file: {algorithm}")
            return
        data = base64.b64decode(bdata)
    except Exception as e:
        print(f"File format error: {e}")
        return

    config = SUPPORTED_ALGOS.get(algorithm)
    if not config:
        print(f"Unsupported algorithm: {algorithm}")
        return
    
    key = derive_key(password, salt, config['key_len'])

    if algorithm == 'aes-256-gcm':
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        try:
            plaintext = decryptor.update(data) + decryptor.finalize()
        except InvalidTag:
            print("Decryption failed: Invalid password or tampered file (GCM Auth failed).")
            return
    elif algorithm == 'aes-128-cbc':
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(data) + decryptor.finalize()
        pad_len = plaintext[-1]
        if pad_len < 1 or pad_len > 16:
            print('Padding error: Bad password or file tampered.')
            return
        plaintext = plaintext[:-pad_len]
    else:
        print('Unsupported algorithm')
        return

    outpath = filepath.replace('.enc','') + '.dec'
    with open(outpath, 'wb') as outf:
        outf.write(plaintext)
    print(f'File decrypted to {outpath}')

def main():
    parser = argparse.ArgumentParser(description='Encrypt or decrypt files with password.')
    parser.add_argument('mode', choices=['encrypt', 'decrypt'], help='Mode: encrypt or decrypt')
    parser.add_argument('filepath', help='Input file path')
    parser.add_argument('-a', '--algorithm', choices=SUPPORTED_ALGOS.keys(), default='aes-256-gcm', help='Encryption algorithm (default: aes-256-gcm)')
    parser.add_argument('-p', '--password', help='Password (if not provided, you will be prompted)')
    args = parser.parse_args()

    if not args.password:
        args.password = getpass.getpass('Password: ')

    if args.mode == 'encrypt':
        if not os.path.exists(args.filepath):
            print('File not found')
            return
        encrypt_file(args.filepath, args.password, args.algorithm)
    else:
        if not os.path.exists(args.filepath):
            print('File not found')
            return
        decrypt_file(args.filepath, args.password)

if __name__ == '__main__':
    main()
