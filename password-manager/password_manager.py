from cryptography.fernet import Fernet
import os
import base64
import hashlib

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_FILE = os.path.join(SCRIPT_DIR, "key.key")
PASSWORDS_FILE = os.path.join(SCRIPT_DIR, "passwords.txt")

def write_key():
    """
    Generates a key and saves it into a file if it doesn't exist.
    """
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)

def load_key():
    """
    Loads the key from the current directory named `key.key`.
    """
    with open(KEY_FILE, "rb") as key_file:
        key = key_file.read()
    return key

def get_fernet(master_pwd):
    """
    Derives a Fernet key from the loaded key and the master password.
    """
    key = load_key()
    # Derive a 32-byte key using SHA256 from the key + master password
    derived = hashlib.sha256(key + master_pwd.encode()).digest()
    fernet_key = base64.urlsafe_b64encode(derived)
    return Fernet(fernet_key)

def view(fer):
    """
    Decrypts and displays all stored passwords.
    """
    if not os.path.exists(PASSWORDS_FILE):
        print("No passwords stored yet.")
        return
        
    with open(PASSWORDS_FILE, 'r') as f:
        lines = f.readlines()
        if not lines:
            print("No passwords stored yet.")
            return
            
        for line in lines:
            data = line.rstrip()
            if "|" not in data:
                continue
            user, enc_passwd = data.split("|", 1)
            try:
                decrypted = fer.decrypt(enc_passwd.encode()).decode()
                print(f"User: {user.strip()} | Password: {decrypted}")
            except Exception:
                print(f"User: {user.strip()} | Password: [Decryption failed]")

def add(fer):
    """
    Adds a new account and encrypted password to the file.
    """
    name = input('Account Name: ').strip()
    pwd = input("Password: ").strip()
    encrypted_pwd = fer.encrypt(pwd.encode()).decode()
    with open(PASSWORDS_FILE, 'a') as f:
        f.write(f"{name} | {encrypted_pwd}\n")

def main():
    write_key()
    master_pwd = input("What is the master password? ")
    fer = get_fernet(master_pwd)

    while True:
        mode = input("Would you like to add a new password or view existing ones (view, add), press q to quit? ").strip().lower()
        if mode == 'q':
            break
        elif mode == "view":
            view(fer)
        elif mode == "add":
            add(fer)
        else:
            print("Invalid mode.")

if __name__ == "__main__":
    main()
