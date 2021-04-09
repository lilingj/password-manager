# rsa加密解密
import rsa
# 序列化对象
import pickle
from typing import List


class RsaObj(object):
    def __init__(self):
        self.public_key = None
        self.private_key = None

    @staticmethod
    def gen_keys(public_key_name="public.key", private_key_name="private.key"):
        """生成新的钥匙对，导出对象到本地"""
        # 生成新的公钥和私钥
        self.public_key, self.private_key = rsa.newkeys(512)
        # 将公钥导出到本地文件
        with open(public_key_name, "wb") as public_file:
            pickle.dump(public_key, public_file)
        # 将私钥导出到本地文件
        with open(private_key_name, "wb") as private_file:
            pickle.dump(private_key, private_file)

    @staticmethod
    def load_obj_from_local(path):
        """从本地文件加载对象"""
        with open(path, "rb") as f:
            # 从文件中读取对象
            obj = pickle.load(f)
            # 将对象返回
            return obj

    def load_public_key(self, public_key="public.key"):
        """加载公钥"""
        self.public_key = self.load_obj_from_local(public_key)
        return self.public_key

    def load_private_key(self, private_key="private.key"):
        """加载私钥"""
        self.private_key = self.load_obj_from_local(private_key)
        return self.private_key

    def load_keys(self, public_key="public.key", private_key="private.key"):
        """读取公钥和私钥, 并返回"""
        self.load_public_key(public_key)
        self.load_private_key(private_key)
        return self.public_key, self.private_key

    def rsa_encrypt(self, message_str, code='utf-8') -> bytes:
        """
        对传入的str字符串加密
        :param message_str: 需要加密的字符串
        :param code: 字符串的编码类型
        :return: 返回加密的字节
        """
        # 从本地读取公钥
        public_key = self.load_public_key()
        # 转成bytes
        content_bytes = message_str.encode(code)
        # 使用公钥加密
        encrypt_content = rsa.encrypt(content_bytes, public_key)
        # 返回加密后的字节
        return encrypt_content

    def rsa_decrypt(self, encrypt_bytes, code='utf-8') -> str:
        """
        使用私钥对加密的bytes进行解密
        :param encrypt_bytes: 加密的内容，bytes类型
        :param code: 字符串的解码类型
        :return: 解密后的字符串
        """
        # 从本地读取私钥
        private_key = self.load_private_key()
        # 使用私钥进行解密
        content_bytes = rsa.decrypt(encrypt_bytes, private_key)
        # utf-8编码
        decrypt_content = content_bytes.decode(code)
        # 返回解密后的字符串
        return decrypt_content


if __name__ == '__main__':
    # 生成公钥和私钥本地, 并初始化rsa对象
    rsa_instance = RsaObj()
    while True:
        # 终端输入
        input_str = input("请输入需要加密的内容：")
        # 当输入是‘exit’时，退出程序
        if input_str == "exit":
            exit()
        # rsa加密
        encrypt_content = rsa_instance.rsa_encrypt(input_str)
        # rsa解密
        content = rsa_instance.rsa_decrypt(encrypt_content)

