from cryptography.fernet import Fernet
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def get_encryption_key():
    try:
        return settings.ENCRYPTION_KEY
    except AttributeError:
        raise ImproperlyConfigured("ENCRYPTION_KEY must be set in settings")

def encrypt_value(value):
    if not value:
        return value
    try:
        f = Fernet(get_encryption_key())
        encrypted_value = f.encrypt(value.encode()).decode()
        return encrypted_value
    except Exception as e:
        print(f"Error encrypting value: {e}")
        return None

def decrypt_value(value):
    if not value:
        return value
    try:
        f = Fernet(get_encryption_key())
        decrypted_value = f.decrypt(value.encode()).decode()
        return decrypted_value
    except Exception as e:
        print(f"Error decrypting value: {e}")
        return None
