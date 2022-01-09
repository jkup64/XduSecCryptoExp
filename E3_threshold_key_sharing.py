import sys
from Crypto.Random.random import randrange, sample
from Crypto.Util.number import getPrime
from E2_Chinese_remainder_theorem import chinese_remainder_theorem

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class KeyShare():
    def __init__(self, number, t, n) -> None:
        self.__num = number
        self.t = t
        self.n = n
    
    def keyShare(self):
        num_len_bin = len(bin(self.__num))
        n_key_parts = []
        M = N = 1 
        for i in range(1, self.n+1):
            d_i = getPrime(num_len_bin // self.t + i)
            k_i = self.__num % d_i
            n_key_parts.append({ "d":d_i, "k":k_i })
            if 1 <= i <= t:
                N *= d_i
            elif (n-t+2) <= i <= self.n:
                M *= d_i

        while(not(M < self.__num < N)):
            n_key_parts = []
            M = N =1 
            for i in range(1, self.n+1):
                d_i = getPrime(num_len_bin // self.t + i)
                k_i = self.__num % d_i
                n_key_parts.append({"d":d_i, "k":k_i})
                if 1 <= i <= t:
                    N *= d_i
                elif (n-t+2) <= i <= self.n:
                    M *= d_i
        print("[Info] N =", N)
        print("[Info] M =", M)
        for i in range(len(n_key_parts)):
            print("[Info] d_{} = {}".format(i+1, n_key_parts[i]["d"]))
        return n_key_parts

    def compoundKey(self, t_key_parts):
        assert len(t_key_parts) >= self.t
        a_list = [x["k"] for x in t_key_parts]
        m_list = [x["d"] for x in t_key_parts]
        revert_key = chinese_remainder_theorem(a_list, m_list)
        print("[Output]",revert_key)
        print("[Output] revert_key == key:"+bcolors.OKBLUE+"{}".format(revert_key == self.__num)+bcolors.ENDC)

def write10Files():
    for file_num in range(1,11):
        with open(sys.path[0] + f"/3_m{file_num}.txt", "w") as file:
            number = randrange(pow(10,500), pow(10,501))
            file.write(str(number))

if __name__ == "__main__":
    write10Files();
    choice_file_num = randrange(1,11)
    with open(sys.path[0] + f"/3_m{choice_file_num}.txt") as choice_file:
        number = int(choice_file.read())
        print("[Input] key is in \"3_m{}.txt\", which is:\n{}".format(choice_file_num, number))
    t = int(input("[Input] t = "))
    n = int(input("[Input] n = "))
    key_share = KeyShare(number, t, n)
    n_key_parts = key_share.keyShare()
    t_key_parts = sample(n_key_parts, t)
    key_share.compoundKey(t_key_parts)
