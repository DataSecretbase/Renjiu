import base64
import json
from Crypto.Cipher import AES


class WXDataCrypt:
    def __init__(self, appid, sessionkey):
        self.appid = appid
        self.sessionkey = sessionkey

    def decrypt(self, encrypteddata, iv):
        """
        :param encrypteddata: 加密数据
        :param iv: 加密向量
        :return: 解密数据
        """
        sessionkey = base64.b64decode(self.sessionkey)
        encrypteddata = base64.b64decode(encrypteddata)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionkey, AES.MODE_CBC, iv)

        res = self._unpad(cipher.decrypt(encrypteddata)).decode('utf-8')
        decrypted = json.loads(res)
        if decrypted['watermark']['appid'] != self.appid:
            raise Exception('Invalid Buffer')

        return decrypted

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
