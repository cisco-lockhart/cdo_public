import array
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding


def encrypt(b64_public_key, text):
    public_key_str = base64.b64decode(b64_public_key)
    public_key = serialization.load_pem_public_key(public_key_str, backend=default_backend())

    return base64.b64encode(public_key.encrypt(text.encode(), padding.PKCS1v15())).decode("utf-8")
