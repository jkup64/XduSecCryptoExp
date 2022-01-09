from math import gcd
from itertools import combinations
import sys


# Python program for the extended Euclidean algorithm
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = egcd(b % a, a)
        return gcd, y - (b // a) * x, x

def chinese_remainder_theorem(a_list, m_list):
    for (x, y) in combinations(m_list, 2):
        if gcd(x, y) != 1:
            print("[Error] gcd({}, {}) != 1 不能直接利用中国剩余定理。".format(x,y))
            return 
    m = 1
    result = 0
    for mi in m_list:
        m *= mi
    for i in range(len(m_list)):
        Mi = m // m_list[i]
        Mi_re = egcd(Mi, m_list[i])[1]
        result += Mi * Mi_re * a_list[i]
        # print("Mi =",Mi,"Mi_re =",Mi_re,"ai =",a_list[i])
    # print("同于方程组的解为：x = {} (mod {})".format(result%m, m))
    return result%m

if __name__ == "__main__":
    with open(sys.path[0] + "/2_m.txt") as amfile:
        a_and_m = [int(i) for i in amfile]
        a_list = a_and_m[:len(a_and_m)//2]
        m_list = a_and_m[len(a_and_m)//2:]
        assert len(a_list) == len(m_list)
    chinese_remainder_theorem(a_list, m_list)
