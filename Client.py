import json
import socket
import sys
import random
from lib import RSA
from lib import AES


if __name__ == "__main__":
    with open("./data/Client/CA_PublicKey.json", 'r') as f:
        CA_PublicKey = json.load(f)
    e_ca, n_ca = CA_PublicKey["KU"]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('localhost', 12345))
    except Exception as e:
        print(f"发生错误：{e}")

    # Client Hello
    rd_num1 = random.randint(0, 1024)
    s.sendall(rd_num1.to_bytes(10, 'big'))

    Certificate = int(s.recv(1024).decode('utf-8'))
    CSR = int(s.recv(1024).decode('utf-8'))
    e, n = json.loads(s.recv(1024).decode('utf-8'))
    rd_num2 = int.from_bytes(s.recv(10), 'big')
    print(f'接收：Certificate:{Certificate}, CSR:{CSR}')
    if not RSA.Encryption(Certificate, e_ca, n_ca) == CSR:
        print("SSL证书不可信，关闭链接！")
        s.close()
        sys.exit()
    else:
        print("SSL证书验证成功！")
        rd_num3 = random.randint(0, 1024)
        pubkey = rd_num1+rd_num2+rd_num3
        encry_rd_num3 = RSA.Encryption(rd_num3, e, n)
        s.sendall(encry_rd_num3.to_bytes(16, 'big'))
        print("Pubkey: ", pubkey)
        pubkey = pubkey.to_bytes(16, 'big')
        data = input()
        while data:
            data = data.encode('utf-8')
            encry_data = AES.aes_encrypt(data, pubkey)
            s.sendall(encry_data)
            recvice = s.recv(1024)
            print("从服务器接收的数据(未解密):", recvice)
            print("从服务器接收的数据(解密后):", AES.aes_decrypt(recvice, pubkey).decode('utf-8'))
            data = input()
        s.close()
