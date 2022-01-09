from Crypto.Util.number import getPrime, inverse, isPrime
from Crypto.Random.random import randrange,randint
from math import gcd

def find_order(p):
    for i in range(2, p+1):
        if gcd(p, i) == 1:
            if (i%p != 1) and (i**2%p !=1 ) and (pow(i, (p-1)//2, p) != 1):
                return i

class EIGamal:
    def __init__(self) -> None:
        p = getPrime(len(bin(10**150)))
        while(isPrime((p-1)//2, 5) == False):
            p = getPrime(len(bin(10**150)))
        self.p = p
        # self.q = (p - 1) // 2
        self.g = find_order(p)
        self.a = randint(100, 200)
        self.ga = pow(self.g, self.a, p)
    
    def encrypt(self, m, p, g, ga):
        k = randrange(1, p-2)
        C1 = pow(g, k, p)
        C2 = (m * pow(ga, k, p)) % p
        return C1,C2
    
    def decrypt(self, C1, C2, p, a):
        V = pow(C1, a, p)
        m = (C2 * inverse(V, p)) % p
        return m

if __name__ == "__main__":
    Eigamal = EIGamal()
    public_key = [Eigamal.p, Eigamal.g, Eigamal.ga]
    private_key = [Eigamal.p, Eigamal.a]
    m = 123456789
    C1,C2 = Eigamal.encrypt(m, public_key[0], public_key[1], public_key[2])
    pt = Eigamal.decrypt(C1, C2, private_key[0], private_key[1])
    print(pt)

