import rsa
import pickle
from typing import List


class RsaObj(object):
    def gen_keys(self, public_key_name="public.key", private_key_name="private.key"):
        self.public_key, self.private_key = rsa.newkeys(512)
        with open(public_key_name, "wb") as public_file:
            pickle.dump(self.public_key, public_file)
        with open(private_key_name, "wb") as private_file:
            pickle.dump(self.private_key, private_file)

    def load_obj_from_local(self, path):
        with open(path, "rb") as f:
            obj = pickle.load(f)
            return obj

    def load_keys(self, public_key="public.key", private_key="private.key"):
        self.public_key = self.load_obj_from_local(public_key)
        self.private_key = self.load_obj_from_local(private_key)

    def rsa_encrypt(self, message_str, code='utf-8') -> bytes:
        return rsa.encrypt(message_str.encode(code), self.public_key)

    def rsa_decrypt(self, encrypt_bytes, code='utf-8') -> str:
        return rsa.decrypt(encrypt_bytes, self.private_key).decode(code)