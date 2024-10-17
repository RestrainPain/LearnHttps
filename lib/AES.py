from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import binascii

# AES对称加密和解密的简单实现

def aes_encrypt(plaintext, key):
    """
    使用AES加密明文。
    参数:
    plaintext: 要加密的明文字符串。
    key: 加密密钥（字节串），长度必须是16（AES-128）、24（AES-192）或32（AES-256）字节。
    返回:
    密文字符串。
    """
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plaintext, AES.block_size))
    iv = cipher.iv
    return binascii.hexlify(iv + ct_bytes)

def aes_decrypt(ciphertext, key):
    """
    使用AES解密密文。
    参数:
    ciphertext: 要解密的密文字符串。
    key: 解密密钥（字节串），长度必须是16（AES-128）、24（AES-192）或32（AES-256）字节。
    返回:
    解密后的明文字符串。
    """
    ct = binascii.unhexlify(ciphertext)
    iv = ct[:16]
    ct = ct[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt


# 示例
if __name__ == "__main__":
    key = get_random_bytes(16)  # 生成一个随机的16字节密钥
    plaintext = "测试消息".encode('utf-8')

    # 加密
    encrypted_text = aes_encrypt(plaintext, key)
    print(f"Encrypted: {encrypted_text}")

    # 解密
    decrypted_text = aes_decrypt(encrypted_text, key)
    print(f"Decrypted: {decrypted_text}")
    print(f"Decrypted: {decrypted_text.decode('utf-8')}")
