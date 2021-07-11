def lf(x, n):
    return ((x - 1) // n)


def dec(c, lam, Mu, n):
    n2 = n * n
    z = lf(pow(c, lam, (n2)), n)
    return ((z * Mu) % n)


def final(c, n):
    return (c) % (n * n)


if __name__ == '__main__':

    c = 4219457669266115004003855340336324083517083509501253934385411411004434841600000
    n = 667 #int(input("n = "))
    lam = 308 #int(input("lam = "))
    Mu = 356 #int(input("Mu = "))
    c1 = final(c, n)
   print(f"c = {c1}")
    s = dec(c, lam, Mu, n)
    print(f"sum of messages = {s}")
