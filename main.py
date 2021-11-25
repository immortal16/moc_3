from functools import reduce
from configparser import ConfigParser


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


def data_parser(path):

    with open(path, mode='r') as file:
        content = file.read().lower()
        num_lines = (content.count('\n') + 1) // 2

    with open(path[:-3] + 'ini', mode='w') as file:
        file.write('[RSA]\n\n')
        file.write(content)

    config = ConfigParser()
    config.read(path[:-3] + 'ini')

    C = []
    N = []

    for i in range(1, num_lines + 1):
        C.append(int(config.get('RSA', f'c{i}'), 16))
        N.append(int(config.get('RSA', f'n{i}'), 16))

    return C, N


def root(x, n):
    high = 1
    mid = 0
    while high ** n <= x:
        high *= 2
    low = high // 2
    while low < high:
        mid = (low + high) // 2
        if low < mid and mid**n < x:
            low = mid
        elif high > mid and mid**n > x:
            high = mid
        else:
            return mid
    return mid + 1


def small_exp(C, N, e):
    c = chinese_remainder(N, C)
    return root(c, e)