import time
EDGE = 0b01111110


def return_rev(black,white,m):
    rev = 0
    if (black|white) & m != 0:
        return rev 
    mask = transfer(m)
    while (mask != 0) and ((mask & white) != 0):
        rev |= mask 
        mask = transfer(mask)
    if (mask & black) == 0:
        return 0
    else:
        return rev 

#着手位置から移動探索するtransferがシフトで
#演算できてしまう以上、もう勝ったも同然では?(フラグ)
#着手可能判定は返り値が0であるか否かで判定、
#その後の反転処理もその返り値で実施

def transfer(m):
    return (m << 1) & EDGE


def count1(n):
    num = 0
    while n != 0 :
        n &= n-1
        num += 1
    return num

def count2(n):
    bin(n).count("1")

if __name__ == "__main__":
    """black = 0b00100000
    white = 0b00011100
    m = 0b00000010
    print(bin(return_rev(black,white,m)))
    m = 0b00000001
    print(bin(return_rev(black,white,m)))
    black = 0b00111110
    white = 0b11000000
    print(bin(return_rev(black,white,m)))
    print("possibility of bug")
    black = 0b00100000
    white = 0b01000000
    m = 0b10000000
    print(bin(return_rev(black,white,m)))
    """
    a = 0b111110011111111110000010101011
    b = 0b000000001100000100000100011111
    c = 0b000000000000000000000000000000
    d = 0b111111111111111111111111111111
    start = time.time()
    print("1",count1(a))
    print("2",count2(a))
    for i in range(100000):
        count1(a)
        count1(b)
        count1(c)
        count1(d)
    print(time.time()-start)
    start = time.time()
    for i in range(100000):
        count2(a)
        count2(b)
        count2(c)
        count2(d)
    print(time.time()-start)