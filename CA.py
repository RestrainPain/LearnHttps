import os.path
import json
from lib import RSA
import Server


if __name__ == "__main__":
    if not os.path.isfile('./data/CA/CA_Keys.json'):
        print("正在创建密钥对")
        RSA.Generate_keys("CA", False)
        print("创建成功")
    with open('./data/CA/CA_Keys.json', 'r') as file:
        CA_keys = json.load(file)
    e, n = CA_keys["KU"]
    d, _ = CA_keys["KR"]
    CA_PublicKey = {"KU": [e, n]}
    with open('./data/Client/CA_PublicKey.json', 'w') as file:
        json.dump(CA_PublicKey, file)

    CSR = Server.getCSR()
    Certificate = RSA.Encryption(CSR, d, n)
    if not os.path.isfile('./data/Server/Certificate.json'):
        with open('./data/Server/Certificate.json', 'w') as file:
            json.dump(Certificate, file)
        print("服务器证书创建成功！")
