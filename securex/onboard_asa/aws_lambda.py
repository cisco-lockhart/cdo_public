# Requires pycryptodome library
import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


def lambda_handler(event, context):
    input_data = json.loads(event["body"])
    key = RSA.importKey(base64.b64decode(input_data["public_key"]).decode("utf-8"))
    encryptor = PKCS1_v1_5.new(key)
    user_crypt = base64.b64encode(encryptor.encrypt(input_data["username"].encode(encoding="UTF-8"))).decode()
    pass_crypt = base64.b64encode(encryptor.encrypt(input_data["password"].encode(encoding="UTF-8"))).decode()

    return {"statusCode": 200, "body": json.dumps({"username": user_crypt, "password": pass_crypt})}
