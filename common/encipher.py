import json
import uuid

from pyDes import des, CBC, PAD_PKCS5
import binascii


# 传出传入的都是字符串

def encrypt(s):
    secret_key = str(uuid.getnode())[0:8]
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en).decode()


def descrypt(s):
    secret_key = str(uuid.getnode())[0:8]
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    return de.decode()


if __name__ == '__main__':
    dict = {'ticket': 'Ki3aRFN2UzbRYD5t', 'jsessionid': '498299EF3CD575AB83B92D7EB217743F',
            'sessionId': 'ltatvr55ovmdqyzodsdbyy45', 'token': '468E363610E74860BFC81C5BD7E5CBAE',
            'username': '2021022121', 'password': 'Cao22222949!'}
    d = encrypt(json.dumps(dict))

    print(d)

    print(json.loads(descrypt(d)))
