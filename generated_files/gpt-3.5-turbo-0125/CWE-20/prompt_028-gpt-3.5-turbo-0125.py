import argparse

def encrypt_file(password, algorithm, file_path):
    # Write code to encrypt the file
    pass

def decrypt_file(password, algorithm, file_path):
    # Write code to decrypt the file
    pass

def main():
    parser = argparse.ArgumentParser(description='CLI for file encryption/decryption')
    parser.add_argument('-p', '--password', help='Password for encryption/decryption')
    parser.add_argument('-a', '--algorithm', help='Algorithm for encryption/decryption')
    parser.add_argument('-f', '--file', help='File path for encryption/decryption')

    args = parser.parse_args()

    if args.password and args.algorithm and args.file:
        encrypt_file(args.password, args.algorithm, args.file)
        decrypt_file(args.password, args.algorithm, args.file)
    else:
        print('Please provide password, algorithm, and file path.')

if __name__ == '__main__':
    main()