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


def data_parser(path, mode):

    cfg = path[:-3] + 'ini'

    with open(path, mode='r') as file:
        content = file.read().lower()
        num_lines = (content.count('\n') + 1) // 2

    with open(cfg, mode='w') as file:
        file.write('[RSA]\n\n')
        file.write(content)

    config = ConfigParser()
    config.read(cfg)

    if mode == 1:

        C = []
        N = []

        for i in range(1, num_lines + 1):
            C.append(int(config.get('RSA', f'c{i}'), 16))
            N.append(int(config.get('RSA', f'n{i}'), 16))

        return C, N

    if mode == 2:

        C = int(config.get('RSA', 'c'), 16)
        N = int(config.get('RSA', 'n'), 16)

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


def small_exp(C, N, e=5):
    c = chinese_remainder(N, C)
    return root(c, e)


def meet_middle(C, N, l=20):
    S = range(1, 2**(l//2) + 1)

    T  = [i for i in S]
    T_ = [pow(i, 65537, N) for i in S]

    for i in S:
        M_s = C * modinv(T_[i], N) % N
        for j in S:
            print(i, j)
            if M_s == T_[j - 1]:
                return i * T[j - 1]

    return 'plaintext was not found'


def task1():
    C, N = data_parser('SE_RSA_1024_5_hard_15.txt', 1)
    M = small_exp(C, N)
    with open('results.txt', mode='w') as file:
        file.write('Task1 M:\n\n')
        file.write(hex(M))


def task2():
    C, N = data_parser('MitM_RSA_2048_20_regular_15.txt.txt', 2)
    M = meet_middle(C, N)
    with open('results.txt', mode='a') as file:
        file.write('\n\nTask2 M:\n\n')
        file.write(hex(M))


#task1()
task2()
