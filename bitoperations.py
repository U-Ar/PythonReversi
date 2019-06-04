EDGE = 0b00000000011111100111111001111110011111100111111001111110000000000
BLACK = 0x0000000810000000
WHITE = 0x0000001008000000
MIN_VALUE = -1000000
MAX_VALUE = 1000000
MAX_BIN = 2 ** 64 - 1

"""
def transfer_e(m):
    return m << 1 & EDGE 

def transfer_ne(m):
    return m >> 7 & EDGE 

def transfer_n(m):
    return m >> 8 & EDGE 

def transfer_nw(m):
    return m >> 9 & EDGE 

def transfer_w(m):
    return m >> 1 & EDGE 

def transfer_sw(m):
    return m << 7 & EDGE 

def transfer_s(m):
    return m << 8 & EDGE 

def transfer_se(m):
    return m << 9 & EDGE

def search_rev_n(black,white,m):
    rev = 0
    mask = transfer_n(m)
    while (mask != 0) and ((mask & white) != 0):
        rev |= mask 
        mask = transfer_n(mask)
    if (mask & black) == 0:
        return 0
    else:
        return rev

def search_rev(black,white,m):
    rev = 0
    if (black|white) & m != 0:
        return rev 
    return search_rev_e(black,white,m) |\
           search_rev_ne(black,white,m) |\
           search_rev_n(black,white,m) |\
           search_rev_nw(black,white,m) |\
           search_rev_w(black,white,m) |\
           search_rev_sw(black,white,m) |\
           search_rev_s(black,white,m) |\
           search_rev_se(black,white,m)   
"""
def get_empty(black,white):
    return 0xffffffffffffffff ^ (black|white)

def get_move_r(black,white,empty,mask,offset):
    e = white & mask 
    m = (black >> offset) & e 
    m |= (m >> offset) & e
    m |= (m >> offset) & e
    m |= (m >> offset) & e
    m |= (m >> offset) & e
    m |= (m >> offset) & e
    return (m >> offset) & empty 

def get_move_l(black,white,empty,mask,offset):
    e = white & mask 
    m = (black << offset) & e 
    m |= (m << offset) & e
    m |= (m << offset) & e
    m |= (m << offset) & e
    m |= (m << offset) & e
    m |= (m << offset) & e
    return (m << offset) & empty

def get_move(black,white):
    topbottommask = 0xffffffffffff
    leftrightmask = 0x7e7e7e7e7e7e7e7e
    empty = get_empty(black,white)
    m = get_move_r(black,white,empty,leftrightmask,1)
    m |= get_move_r(black,white,empty,leftrightmask,7)
    m |= get_move_r(black,white,empty,topbottommask,8)
    m |= get_move_r(black,white,empty,leftrightmask,9)
    m |= get_move_l(black,white,empty,leftrightmask,1)
    m |= get_move_l(black,white,empty,leftrightmask,7)
    m |= get_move_l(black,white,empty,topbottommask,8)
    m |= get_move_l(black,white,empty,leftrightmask,9)
    return m

def get_rev_r(black,white,move,mask,offset):
    e = white & mask
    m = (move << offset) & e
    m |= (m << offset) & e 
    m |= (m << offset) & e 
    m |= (m << offset) & e 
    m |= (m << offset) & e    
    m |= (m << offset) & e 
    o = (black >> offset) & e 
    o |= (o >> offset) & e
    o |= (o >> offset) & e
    o |= (o >> offset) & e
    o |= (o >> offset) & e
    o |= (o >> offset) & e
    return m & o

def get_rev_l(black,white,move,mask,offset):
    e = white & mask
    m = (move >> offset) & e
    m |= (m >> offset) & e 
    m |= (m >> offset) & e 
    m |= (m >> offset) & e 
    m |= (m >> offset) & e    
    m |= (m >> offset) & e 
    o = (black << offset) & e 
    o |= (o << offset) & e
    o |= (o << offset) & e
    o |= (o << offset) & e
    o |= (o << offset) & e
    o |= (o << offset) & e
    return m & o

def get_rev(black,white,move):
    topbottommask = 0xffffffffffff
    leftrightmask = 0x7e7e7e7e7e7e7e7e
    m = get_rev_r(black,white,move,leftrightmask,1)
    m |= get_rev_r(black,white,move,leftrightmask,7)
    m |= get_rev_r(black,white,move,topbottommask,8)
    m |= get_rev_r(black,white,move,leftrightmask,9)
    m |= get_rev_l(black,white,move,leftrightmask,1)
    m |= get_rev_l(black,white,move,leftrightmask,7)
    m |= get_rev_l(black,white,move,topbottommask,8)
    m |= get_rev_l(black,white,move,leftrightmask,9)
    return m

def bit_count(n):
    return bin(n).count("1")

def lowest_onebit(n):
    return n & (~n+1)

def delete_lowest(bit,lowest):
    return bit ^ lowest
    
def value_func_static(black,white,parameter=1):
    """
    value_map =       ((30,-12, 0,-1,-1, 0,-12,30),
                     (-12,-15,-3,-3,-3,-3,-15,-12),
                     ( 0,-3, 0,-1,-1, 0,-3, 0),
                     (-1,-3,-1,-1,-1,-1,-3,-1),
                     (-1,-3,-1,-1,-1,-1,-3,-1),
                     ( 0,-3, 0,-1,-1, 0,-3, 0),
                     (-12,-15,-3,-3,-3,-3,-15,-12),
                     (30,-12, 0,-1,-1, 0,-12,30))"""
                     # 0  1  1
                     # 1  1  0
                     # 1  0  1
    value = 0
    value += bit_count(get_move(black,white))
    value -= bit_count(get_move(black,white))
    value -= parameter*2*(bit_count(black&0x4281000000008142))
    value += parameter*2*(bit_count(white&0x4281000000008142))
    value += parameter*(bit_count(black&0x2400810000810024))
    value -= parameter*(bit_count(white&0x2400810000810024))
    value += parameter*10*(bit_count(black&0x8100000000000081))
    value -= parameter*10*(bit_count(white&0x8100000000000081))
    return value

def value_func_basic(black,white):
    b = bit_count(black)
    w = bit_count(white)
    return b - w

import random 
def value_func_random(black,white):
    return random.random()

def alphabeta_first(black,white,depth,limit):
    if depth == 0:
        return value_func_static(black,white),[]
    value = MIN_VALUE
    move = []
    moves = get_move(black,white)
    move = lowest_onebit(moves)
    while move != 0:
        rev = get_rev(black,white,move)
        v,m = alphabeta_second(black^(rev|move),white^rev,depth,limit)
        if v > value:
            if v > limit:
                return m,v 

        

        moves = delete_lowest(moves,move)
        move = lowest_onebit(moves)
    return value,move

def alphabeta_second(black,white,depth,limit):
    if depth == 0:
        return value_func_static(black,white),[]
    value = MAX_VALUE
    move = []
    moves = get_move(white,black)
    move = lowest_onebit(moves)
    while move != 0:
        rev = get_rev(white,black,move)

        moves = delete_lowest(moves,move)
        move = lowest_onebit(moves)
    return value,move 

#目標:value_funcを選択可能にする(引数に評価関数をぶち込む)
"""def bit_negamax(black,white,depth,alpha,beta,alreadypassed):
    if depth == 0:
        return value_func_static(black,white),[],False
    value = alpha
    own_move = []
    moves = get_move(black,white)
    move = lowest_onebit(moves)
    passed = True 
    while move != 0:
        passed = False
        rev = get_rev(black,white,move)
        v,m,a = bit_negamax(white^rev,black^(rev|move),depth-1,-beta,-value,False)
        if not a:
            m = []
        v *= -1
        if v > value:
            if v >= beta:
                return v, [move]+own_move ,False
            value = v 
            own_move = [move] + m
        moves = delete_lowest(moves,move)
        move = lowest_onebit(moves)
    if passed and alreadypassed:
        return value_func_static(black,white),[],True
    elif passed:
        v,m,_ = bit_negamax(white,black,depth,-beta,-value,passed)
        return -v,m,True
    else:
        return value,own_move,False"""

def bit_negamax(black,white,depth,alpha,beta,alreadypassed,value_func):
    if depth == 0:
        return value_func(black,white),[],False
    value = alpha
    own_move = []
    moves = get_move(black,white)
    move = lowest_onebit(moves)
    passed = True 
    while move != 0:
        passed = False
        rev = get_rev(black,white,move)
        v,m,a = bit_negamax(white^rev,black^(rev|move),depth-1,-beta,-value,False,value_func)
        if not a:
            m = []
        v *= -1
        if v > value:
            if v >= beta:
                return v, [move]+own_move ,False
            value = v 
            own_move = [move] + m
        moves = delete_lowest(moves,move)
        move = lowest_onebit(moves)
    if passed and alreadypassed:
        return value_func(black,white),[],True
    elif passed:
        v,m,_ = bit_negamax(white,black,depth,-beta,-value,passed,value_func)
        return -v,m,True
    else:
        return value,own_move,False

def board_to_bit(board):
    black = 0
    white = 0
    for i in range(7,-1,-1):
        for j in range(7,-1,-1):
            if board[i][j] == True:
                black += 1
            elif board[i][j] == False:
                white += 1
            black = black << 1
            white = white << 1
    return black >> 1 , white >> 1

def co_to_bit(co):
    return 8 * co[0] + co[1]

def bit_to_co(bit):
    i = 0
    while bit & 1 == 0:
        bit = bit >> 1
        i += 1
    return i // 8 , i % 8 

def bit_to_board(black,white):
    board = [[None]* 8 for i in range(8)]
    for i in range(64):
        b = black & 1
        w = white & 1
        board[i//8][i%8] = (b==1) if b != w else None  
        black = black >> 1
        white = white >> 1
    return board

def print_board(black,white):
    for _ in range(8):
        row = ""
        for __ in range(8):
            b = black & 1
            w = white & 1
            if b or w:
                row += ("● ","○ ")[b]
            else:
                row += "   "
            black = black >> 1
            white = white >> 1
        print(row)

def play_test(first_depth, second_depth):
    black = BLACK
    white = WHITE
    color = True
    i = 0
    print_board(black,white)
    while True:
        i += 1
        print(i)
        print(["WHITE","BLACK"][color])
        if color:
            _,move,__ = bit_negamax(black,white,first_depth,MIN_VALUE,MAX_VALUE,False)
            for m in move:
                rev = get_rev(black,white,m)
                black ^= (m|rev)
                white ^= rev
                print_board(black,white)
        else:
            _,move,__ = bit_negamax(white,black,second_depth,MIN_VALUE,MAX_VALUE,False)
            for m in move:
                rev = get_rev(white,black,m)
                white ^= (m|rev)
                black ^= rev
                print_board(black,white)
        if get_move(black,white)==0 and get_move(white,black)==0:
            print(get_move(black,white),get_move(white,black))
            print("BLACK: "+str(bit_count(black))+"WHITE: "+str(bit_count(white)))
            return None
        color = not color


if __name__ == "__main__":
    NONE = None
 
    BOARD = [[NONE,NONE,NONE,NONE,NONE,NONE,NONE,NONE],
         [NONE,NONE,NONE,NONE,NONE,NONE,NONE,NONE],
         [NONE,NONE,NONE,NONE,NONE,NONE,NONE,NONE],
         [NONE,NONE,NONE,NONE,NONE,NONE,NONE,NONE],
         [NONE,NONE,NONE,NONE,NONE,NONE,NONE,NONE],
         [NONE,NONE,NONE,NONE,NONE,NONE,NONE,NONE],
         [NONE,NONE,NONE,NONE,NONE,NONE,NONE,NONE],
         [NONE,NONE,NONE,NONE,NONE,NONE,NONE,True],]
    
    print(bit_to_co(board_to_bit(BOARD)[0]))
