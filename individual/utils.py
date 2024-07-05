import json
from cryptography.fernet import Fernet


key = Fernet.generate_key()
cipher_suite = Fernet(key)


def encrypt_data(data):
    json_data = json.dumps(data)
    encrypted_data = cipher_suite.encrypt(json_data.encode())
    return encrypted_data.decode()


def decrypt_data(encrypted_data):
    decrypted_data = cipher_suite.decrypt(encrypted_data.encode())
    return json.loads(decrypted_data.decode())
