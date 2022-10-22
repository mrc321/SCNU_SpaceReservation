import json
import os

from common import encipher

def read():
    try:
        if os.path.exists('user.dat'):
            # 先直接从文件中读取，并且检验是否有效
            with open('user.dat', 'r', encoding='utf-8') as f:
                cookieInfo = json.loads(encipher.descrypt(f.read()))
                return cookieInfo
        else:
            # 文件不存在就直接返回
            return None
    except Exception as e:
        print(e)
        return None

def write(dict):
    with open('user.dat', 'w', encoding='utf-8') as f:
        f.write(encipher.encrypt(json.dumps(dict)))
        print("写入成功")