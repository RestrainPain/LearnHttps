import json


def generate_primes(n: int):

    sieve = [True] * (n+1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5)+1):
        if sieve[i]:
            for j in range(i*i, n+1, i):
                sieve[j] = False
    return [i for i in range(n//2, n+1) if sieve[i]]


if __name__ == "__main__":

    n = 2**16
    primes = generate_primes(n)
    print(primes)
    primes_dict = {"primes": primes}
    primes_str = json.dumps(primes_dict)
    with open('../data/primes16.json', 'w') as file:
        json.dump(primes_dict, file)

