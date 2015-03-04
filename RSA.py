#!/usr/bin/python

from random import randrange, getrandbits, randint

def encrypt(m, e, n):
    return pow(m, e, n)

def decrypt(c, d, p, q):
    #return pow(c, d, p*q)
    return chineseRemainderTheorem(c, d, p, q)

def chineseRemainderTheorem(c, d, p, q):        
    m1 = pow(c, d % (p - 1), p)
    m2 = pow(c, d % (q - 1), q)

    y1, y2 = getY1Y2(p, q)

    return (m1 * y2 * q + m2 *y1 * p) % (p*q)

def getY1Y2(p, q):
    return exendedEucledeanAlgorithm(p, q)[1:]

def find_prime(n):
    number = getrandbits(n)

    while not isProbablePrime(number):
        number = getrandbits(n)

    return number

def isProbablePrime(n, t = 7):
    """
    Miller-Rabin primality test
    """
    if n < 2:
        return False

    if n == 2:
        return True

    if (n % 2 == 0):
        return False

    d, s = calcDAndSForPrimeTest(n)

    for i in range(t):
        a = randrange(2,n)
        while not isRelativePrime(n, a):
            a = randrange(2,n)
        if try_composite(a, n, d, s):
            return False

    return True

def calcDAndSForPrimeTest(n):
    s = 0
    d = n-1

    while True:
        quotient, remainder = divmod(d, 2)
        if remainder == 1:
            break
        s += 1
        d = quotient

    return (d, s)

def try_composite(a, n, d, s):
    if pow(a, d, n) == 1:
        return False
    for i in range(s):
        if pow(a, 2**i * d, n) == n-1:
            return False
    return True

def calculatePhiN(p,q):
    return (p-1) * (q-1)

def choose_e(PhiN):
    e = randrange(2, PhiN)
    while not isRelativePrime(e, PhiN):
        e = randrange(2, PhiN)

    return e

def genRSAKeys(bitLenght):
    p = find_prime(bitLenght/2)
    q = find_prime(bitLenght/2)

    while p == q or calculatePhiN(p, q) == 2:
        q = find_prime(bitLenght/2)

    if q > p:
        q, p = p, q

    n = p*q
    PhiN = calculatePhiN(p, q)
    e = choose_e(PhiN)

    d = getD(PhiN, e)

    return ((e,n),(d,p,q,PhiN))

def getD(PhiN, e):
    return exendedEucledeanAlgorithm(PhiN, e)[2]

def isRelativePrime(x, y):
    if exendedEucledeanAlgorithm(x, y)[0] == 1:
        return True
    return False

def exendedEucledeanAlgorithm(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def main():
    ((e,n), (d, p, q, PhiN)) = genRSAKeys(2048)

    print "Public keys: e = {0}, n = {1}".format(e, n)
    print "Private keys: d = {0}, p = {1}, q = {2}, PhiN = {3}\n".format(d, p, q, PhiN)

    while True:
        try:
            m = int(raw_input("Message: ")) % n
        
        except ValueError:
            print "Error! Only works with numbers. (Enter '0' to quit)"
            continue

        if m == 0:
            break

        c = encrypt(m, e, n)
        decM = decrypt(c, d, p, q)

        print "c = {0}, dec(c) = {1}".format(c, decM)
        
        if decM != m:
            print "Something wrong!"
            return False

if __name__ == "__main__":
    main()