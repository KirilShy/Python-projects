# Password Manager

A simple command-line password manager that securely stores and retrieves passwords using encryption.

## Features
- Secure password storage using Fernet encryption
- Master password protection
- Add and view stored passwords
- Passwords are stored locally in an encrypted format

## Setup
1. Make sure you have Python installed
2. Install required packages:
   ```
   pip install cryptography
   ```
3. Run the program:
   ```
   python password_manager.py
   ```

## Usage
1. When you first run the program, it will ask for a master password
2. Choose between two modes:
   - `add`: Add a new account and password
   - `view`: View all stored passwords
   - `q`: Quit the program

## Security Notes
- The `key.key` and `passwords.txt` files are not tracked in git for security reasons
- Keep your master password safe and don't share it
- The program will create these files automatically when you first run it 