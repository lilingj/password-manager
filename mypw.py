import random
import pickle
import string
from typing import List

import myrsa

class MyPW:
    def __init__(self, url, username, password, note):
        self.url = url
        self.username = username
        self.password = password
        self.note = note
        self.is_encrypted = False

    def __str__(self):
        ret  = "┏-----------------------------------------┓\n"
        if self.is_encrypted:
            ret += "┣━ 全文加密"
        
        ret += "┣━ url:      " + str(self.url) + "\n"
        ret += "┣━ username: " + str(self.username) + "\n"
        ret += "┣━ password: " + str(self.password) + "\n"
        ret += "┣━ note:     " + str(self.note) + "\n"
        ret += "┗-----------------------------------------┛\n"
        return ret

    def format_str(self, id):
        return "|{:4d}|{:20s}|{:20s}|{:20s}|{:20s}|".format(id, str(self.url), str(self.username), str(self.password), str(self.note))

    def gen_pw(self):
        self.password = \
            random.sample(string.ascii_letters, 5) + \
            random.sample(string.digits, 5) + \
            random.sample("""!"#$%&'()*+,-./:;<=>?@[\]^_{|}~""", 5)
        random.shuffle(self.password)
        self.password = "".join(self.password)
	    

    def encrypt(self, rsa_obj: myrsa.RsaObj) -> None:
        self.is_encrypted = True
        salt = "salt:" + str(random.random())[:10]

        def _encrypt(s: str):
            return rsa_obj.rsa_encrypt(s + salt)

        self.url = _encrypt(self.url)
        self.username = _encrypt(self.username)
        self.password = _encrypt(self.password)
        self.note = _encrypt(self.note)

    def decrypt(self, rsa_obj: myrsa.RsaObj) -> None:
        self.is_encrypted = False

        def _decrypt(c: bytes):
            return rsa_obj.rsa_decrypt(c)[:-15]

        self.url = _decrypt(self.url)
        self.username = _decrypt(self.username)
        self.password = _decrypt(self.password)
        self.note = _decrypt(self.note)



def store_mypws(mypws: List[MyPW], file_name = "pwdb.pkl"):
    with open(file_name, "wb") as f:
        pickle.dump(mypws, f)

def load_mypws(file_name = "pwdb.pkl") -> List[MyPW]:
    obj = []
    with open(file_name, "rb") as f:
        obj = pickle.load(f)
    return obj

            





    