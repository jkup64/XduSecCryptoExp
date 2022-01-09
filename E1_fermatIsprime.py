import sys
from math import gcd
from Crypto.Random.random import randrange

def fermat_isprime(m, k):
    # 给定奇整数m>=3和安全参数k
    assert(m>=3 and m%2==1)
    buffer_a = []
    for i in range(1,k+1):

        # 1) 随机选取整数a, 2<=a<=m-2
        a = randrange(2,m-1)
        while(buffer_a.count(a) != 0):
            a = randrange(2,m-1)
        buffer_a.append(a)
        print("[Info] k = {}\ta ={}".format(i,a), end="\t")
    

        # 2) 计算g =（a,m）,如果g=1,转(3)；否则，跳出，m为合数
        g = gcd(a,m)
        if(g != 1):
            print("g = 1\n[Result] m是合数")
            return

        # 3) 计算r=a^{m-1}(mode m)，如果r=1,m可能是素数，转（1）；否则，跳出，m为合数。
        r = pow(a,(m-1),m)
        if(r != 1):
            print("r = 1\n[Result] m是合数")
            return 
        print("m为素数的概率为：{}".format(1-1/(2**i)))

    # 4)重复上述过程k次，如果每次得到m可能为素数，则m为素数的概率为1-\frac{1}{2^k}
    print("[Result] m为素数的概率为：{}".format(1-1/(2**k)))
    return

if __name__ == "__main__":
    with open(sys.path[0]+"/1_m.txt") as mesfile:
        m_list = [int(line) for line in mesfile.readlines()]
    k = int(input("设定：安全系数k = "))
    for i,m in enumerate(m_list):
        print("\n:: ==> Test[{}] \nm = {}".format(i+1,m))
        fermat_isprime(m,k)
