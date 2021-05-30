import math
import sympy
from random import randint

def lf(x, n):
    return ((x - 1) // n)


def enc(g, m, n):
    r = randint(1, n)
    while math.gcd(r, n) != 1:
        r = randint(1, n)
    n2 = n * n
    return ((g ** m) * (r ** n)) % n2


def mod_Inv(x, y):
    for i in range(y):
        if (x * i) % y == 1:
            return i
    return -1


def MuWithoutInverse(lam, n2):
    g = randint(1, n2)
    z = pow(g, lam, n2)
    l = lf(z, n)
    ln = mod_Inv(l, n)
    return ln, g


if __name__ == '__main__':

    p = sympy.randprime(100, 500)
    q = sympy.randprime(100, 500)

    while math.gcd((p * q), ((p - 1) * (q - 1))) != 1 or p == q:
        p = sympy.randprime(100, 500)
        q = sympy.randprime(100, 500)
    else:
        p = p
        q = q

    n = p * q
    n2 = pow(n, 2)

    lam = math.lcm((p - 1), (q - 1))

    ln, g = MuWithoutInverse(lam, n2)

    while ln == -1:
        ln, g = MuWithoutInverse(lam, n2)

    Mu = ln % n

    m = 23
#    print(f"Plaintext message, m = {m}")

    c = enc(g, m, n)
    c = c % n
