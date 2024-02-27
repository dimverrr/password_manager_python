import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key


def encrypt(password):
    password_to_encrypt = str(password).encode("utf-8")
    load_dotenv()

    key = os.getenv("SECRET_KEY")
    if not key:
        key = Fernet.generate_key()
        set_key(".env", "SECRET_KEY", key.decode("utf-8"))
    f = Fernet(key=key)
    encrypted_password = f.encrypt(password_to_encrypt)
    return encrypted_password


def decrypt(password):
    load_dotenv()

    key = os.getenv("SECRET_KEY")
    f = Fernet(key=key)
    decrypted_password = f.decrypt(eval(password))
    return decrypted_password
