from functools import reduce


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def chinese_remainder(N, A):
    summ = 0
    prod = reduce(lambda x, y: x * y, N)
    for n, a in zip(N, A):
        p = prod // n
        summ += a * modinv(p, n) * p
    return summ % prod
