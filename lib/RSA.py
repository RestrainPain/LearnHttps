import os.path
import json
import random


def Generate_keys(name: str, isClient: bool=True):
    with open('./data/primes16.json', 'r') as file:
        primes_dict: dict = json.load(file)
    primes = primes_dict["primes"]
    length = primes.__len__()
    index_p = random.randint(0, length-2)
    index_q = random.randint(index_p+1, length-1)
    index_e = random.randint(index_q, length)
    p = primes[index_p]
    q = primes[index_q]
    e = primes[index_e]
    n = p*q
    phi_n = (p-1)*(q-1)

    k = 1
    while True:
        tmp = (k*phi_n+1) % e
        if tmp == 0:
            d = (k*phi_n+1) // e
            break
        k += 1
    keys = {"KU": [e, n], "KR": [d, n]}

    if not isClient:
        path = f"./data/{name}"
    else:
        path = "./data/Client"
    if not os.path.exists(path):
        os.makedirs(path)
    path = path + f"/{name}_Keys.json"
    with open(path, 'w') as file:
        json.dump(keys, file)

    return keys


def Encryption(m: int, e: int, n: int):
    c = pow(m, e, n)
    return c


def Decryption(c: int, d: int, n: int):
    m = pow(c, d, n)
    return m


if __name__ == "__main__":
    # Generate_keys('test', True)
    m = random.randint(2, 2**30)
    with open("../data/Client/test_Keys.json", 'r') as file:
        keys = json.load(file)
    e, n = keys["KU"]
    d, _ = keys["KR"]
    print(keys)
    encode_m = Encryption(m, e, n)
    decode_c = Decryption(encode_m, d, n)
    print(m)
    print(decode_c)
