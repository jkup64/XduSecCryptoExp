import sys
from Crypto.Random.random import randrange
from Crypto.Util.number import bytes_to_long, inverse, long_to_bytes
from Crypto.Hash import SHA256, SHAKE256

# SM2 椭圆曲线公钥密码加解密python实现
# F_p-256曲线
p = int("".join("8542D69E 4C044F18 E8B92435 BF6FF7DE 45728391 5C45517D 722EDB8B 08F1DFC3".split()), base = 16)
a = int("".join("787968B4 FA32C3FD 2417842E 73BBFEFF 2F3C848B 6831D7E0 EC65228B 3937E498".split()), base = 16)
b = int("".join("63E4C6D3 B23B0C84 9CF84241 484BFE48 F61D59A5 B16BA06E 6E12D1DA 27C5249A".split()), base = 16)
n = int("".join("8542D69E 4C044F18 E8B92435 BF6FF7DD 29772063 0485628D 5AE74EE7 C32E79B7".split()), base = 16)
h = 1 # 余因子 
G = [
    int("".join("421DEBD6 1B62EAB6 746434EB C3CC315E 32220B3B ADD50BDC 4C4E6C14 7FEDD43D".split()), base = 16),
    int("".join("0680512B CBB42C07 D47349D2 153B70C4 E5D7FDFC BFA36EA1 A85841B9 E46E09A2".split()), base = 16)
]

class bcolors:
    HEADER = '\033[95m'     #紫色
    OKBLUE = '\033[94m'     #蓝色
    OKCYAN = '\033[96m'     #亮蓝色
    OKGREEN = '\033[92m'    #绿色
    WARNING = '\033[93m'    #黄色
    FAIL = '\033[91m'       #红色
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def addPoint(P1, P2):
    if (P1[0] == P2[0]) and (P1[1] == P2[1]):
        # 倍点运算
        lamd = (3 * P1[0] * P1[0] + a) * inverse(2 * P1[1], p) % p
    else:
        # 点加运算
        lamd = (P2[1] - P1[1]) * inverse(P2[0] - P1[0], p) % p
    P3 = []
    P3.append((lamd * lamd - P1[0] - P2[0]) % p) # the priority of % is higher than  +/-
    P3.append((lamd * (P1[0] - P3[0]) - P1[1]) % p)
    return P3

def nPoint(k, P):
    bin_k = bin(k)[2:]
    temp_P = P
    get_1 = False   # The frist getting 1 while scanning bin_k
    for i in range(len(bin_k)-1, -1 ,-1):
        if (bin_k[i] == '1') and (get_1 == True):   # is '1' <type:str>
            res_P = addPoint(res_P, temp_P)
        elif (bin_k[i] == '1') and (get_1 == False):
            res_P = temp_P
            get_1 = True
        temp_P = addPoint(temp_P, temp_P)
    return res_P

def kdf(bytes_input, klen):
    return SHAKE256.new(bytes_input).read(klen)

def bytesXor(a, b):
    assert len(a) == len(b)
    return bytes([a[i]^b[i] for i in range(len(a))])

class CryptoSM2():
    def __init__(self) -> None:
        # 产生密钥
        dB = randrange(1, n) # sk
        pB = nPoint(dB, G)   # pk
        self.sk = dB
        self.pk = pB
    
    def encrypt(self, M):
        bytes_M = M.encode("utf-8")
        klen = len(bytes_M)
        # A1
        k = randrange(1, n)
        # A2
        point_C1 = nPoint(k, G)
        C1 = long_to_bytes(point_C1[0]) + long_to_bytes(point_C1[1])
        # A3
        hPB = nPoint(h, self.pk)    # pk is pB
        assert (hPB[1]**2) % p == (hPB[0]**3 + a*hPB[0] + b) % p
        # A4
        kPB = nPoint(k, self.pk)    # pk is PB
        bin_x2y2 = long_to_bytes(kPB[0]) + long_to_bytes(kPB[1])
        # A5
        t = kdf(bin_x2y2, klen)
        while all(t[i] == 0 for i in range(len(t))):
            # A1
            k = randrange(1, n)
            # A2
            point_C1 = nPoint(k, G)
            C1 = long_to_bytes(point_C1[0]) + long_to_bytes(point_C1[1])
            # A3
            hPB = nPoint(h, self.pk)    # pk is pB
            assert (hPB[1]**2) % p == (hPB[0]**3 + a*hPB[0] + b) % p
            # A4
            kPB = nPoint(k, self.pk)    # pk is PB
            bin_x2y2 = long_to_bytes(kPB[0]) + long_to_bytes(kPB[1])
            # A5
            t = kdf(bin_x2y2, klen)
        # A6
        C2 = bytesXor(bytes_M, t)
        # A7
        hash2 = SHA256.new(long_to_bytes(kPB[0]) + bytes_M + long_to_bytes(kPB[1]))
        C3 = hash2.digest()
        # A8
        return C1, C2, C3, klen

    def decrypt(self, C1, C2, C3, klen):
        # B1
        x1 = bytes_to_long(C1[:len(C1)//2])
        y1 = bytes_to_long(C1[len(C1)//2:])
        assert (y1**2) % p == (x1**3 + a*x1 +b) % p
        # B2
        hC1 = nPoint(h, [x1, y1])
        assert (hC1[1]**2) % p == (hC1[0]**3 + a*hC1[0] + b) % p
        # B3
        dBC1 = nPoint(self.sk, [x1, y1])  # sk is dB
        x2 = long_to_bytes(dBC1[0])
        y2 = long_to_bytes(dBC1[1])
        # B4
        t = kdf(x2 + y2, klen)
        assert any(t[i] != 0 for i in range(len(t)))
        # B5
        M_prime = bytesXor(C2, t)
        hash2 = SHA256.new(x2 + M_prime + y2)
        # B6
        u = hash2.digest()
        assert u == C3
        return M_prime.decode("utf-8")

if __name__ == "__main__":
    with open(sys.path[0] + "/5_m1.txt") as pt_file:
        M = pt_file.read().strip()
    SM2 = CryptoSM2()
    C1, C2, C3, klen = SM2.encrypt(M)
    M_prime = SM2.decrypt(C1, C2, C3, klen)
    
    print(bcolors.BOLD + "[Info]" + bcolors.ENDC + " p =", p)
    print(bcolors.BOLD + "[Info]" + bcolors.ENDC + " a =", a)
    print(bcolors.BOLD + "[Info]" + bcolors.ENDC + " b =", b)
    print(bcolors.BOLD + "[Info]" + bcolors.ENDC + " n =", n)
    print(bcolors.BOLD + "[Info]" + bcolors.ENDC + " h =", h)
    print(bcolors.BOLD + "[Info]" + bcolors.ENDC + " G[x] =", G[0])
    print(bcolors.BOLD + "[Info]" + bcolors.ENDC + " G[y] =", G[1])
    print(bcolors.BOLD + "[Info]" + bcolors.ENDC + " C  =", C1 + C2 + C3)
    print(bcolors.OKBLUE + "[Result]" + bcolors.ENDC + " M  =", M)
    print(bcolors.OKBLUE + "[Result]" + bcolors.ENDC + " M' =", M_prime)
    if M_prime == M:
        print(bcolors.OKGREEN + "[Result] OK" + bcolors.ENDC )
    else:
        print(bcolors.FAIL + "[Result] FAIL" + bcolors.ENDC )