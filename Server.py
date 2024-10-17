import socket
import threading
import json
import random
from lib import RSA
from lib import AES


def getCSR():
    CSR = 1234567
    return CSR


def get_Keys():
    with open("./data/Server/Server_Keys.json", 'r') as f:
        keys = json.load(f)
    return keys


def get_Certificate():
    with open("./data/Server/Certificate.json", 'r') as f:
        Certificate = json.load(f)
    return Certificate


def keyboard_listener(server_socket):
    while True:
        user_input = input()
        if user_input.lower() == 'stop':
            print("正在停止服务器...")
            server_socket.close()
            break


def handle_client(client_socket: socket, client_address):
    try:
        print(f"与 {client_address} 的连接已建立")
        print("正在进行SSL证书验证")

        # Server Hello
        rd_num1 = int.from_bytes(client_socket.recv(10), 'big')
        client_socket.sendall(json.dumps(Certificate).encode('utf-8'))
        client_socket.sendall(json.dumps(CSR).encode('utf-8'))
        client_socket.sendall(json.dumps(keys['KU']).encode('utf-8'))
        rd_num2 = random.randint(0, 1024)
        client_socket.sendall(rd_num2.to_bytes(10, 'big'))
        encry_rd_num3 = client_socket.recv(1024)

        if encry_rd_num3:
            print("验证成功")
            rd_num3 = RSA.Decryption(int.from_bytes(encry_rd_num3, 'big'), d, n)
            pubkey = rd_num1+rd_num2+rd_num3
            print("Pubkey: ", pubkey)
            pubkey = pubkey.to_bytes(16, 'big')
            while True:
                encry_data: bytes = client_socket.recv(1024)
                data = AES.aes_decrypt(encry_data, pubkey)
                data = data.decode('utf-8')
                print(f"来自{client_address}: {data}")
                client_socket.sendall(AES.aes_encrypt(data.encode('utf-8'), pubkey))

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        print(f"与 {client_address} 的连接已关闭")


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    keyboard_thread = threading.Thread(target=keyboard_listener, args=(server_socket,))
    keyboard_thread.daemon = True
    keyboard_thread.start()
    print(f"服务器在 {host}:{port}上监听")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except OSError as e:
        # 当socket关闭时，accept()会抛出OSError
        if e.winerror == 10038:
            print("服务器端口已关闭")
        else:
            raise
    finally:
        server_socket.close()
        print("服务器已停止")


if __name__ == "__main__":
    Certificate = get_Certificate()
    CSR = getCSR()
    keys = get_Keys()
    e, n = keys["KU"]
    d, _ = keys["KR"]
    start_server('localhost', 12345)
