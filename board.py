from itertools import product
NONE = None
BLACK = True
WHITE = False

NORMAL = 0
PASS = 1
GAMEOVER = 2

BOARD = [[NONE,NONE,NONE,NONE,NONE,NONE,NONE,NONE],
         [NONE,NONE,NONE,NONE,NONE,NONE,NONE,NONE],
         [NONE,NONE,NONE,NONE,NONE,NONE,NONE,NONE],
         [NONE,NONE,NONE,WHITE,BLACK,NONE,NONE,NONE],
         [NONE,NONE,NONE,BLACK,WHITE,NONE,NONE,NONE],
         [NONE,NONE,NONE,NONE,NONE,NONE,NONE,NONE],
         [NONE,NONE,NONE,NONE,NONE,NONE,NONE,NONE],
         [NONE,NONE,NONE,NONE,NONE,NONE,NONE,NONE],]

#デバッグ用評価関数の呼び出し回数
count = 0


class Board:
    def __init__(self, b):
        self.board = b[:]
        self.reversed_list = []
        self.reversed_record = []
        self.co_record = []
        self.color_record = []
        self.record_pointer = 0
    
    def initialize(self,b):
        self.board = b[:]
        self.reversed_list = []
        self.reversed_record = []
        self.co_record = []
        self.color_record = []
        self.record_pointer = 0

    def check_n(self,color,co):
        x = co[0]
        y = co[1]
        if x <= 1:
            return False
        x -= 1
        while self.board[x][y] == (not color):
            if self.board[x-1][y] == color:
                return True
            if self.board[x-1][y] is NONE:
                return False
            if x == 1:
                return False
            x -= 1
        return False

    def check_e(self,color,co):
        x = co[0]
        y = co[1]
        if y >= 6:
            return False
        y += 1
        while self.board[x][y] == (not color):
            if self.board[x][y+1] == color:
                return True
            if self.board[x][y+1] is NONE:
                return False
            if y == 6:
                return False
            y += 1
        return False

    def check_s(self,color,co):
        x = co[0]
        y = co[1]
        if x >= 6:
            return False
        x += 1
        while self.board[x][y] == (not color):
            if self.board[x+1][y] == color:
                return True
            if self.board[x+1][y] is NONE:
                return False
            if x == 6:
                return False
            x += 1
        return False

    def check_w(self,color,co):
        x = co[0]
        y = co[1]
        if y <= 1:
            return False
        y -= 1
        while self.board[x][y] == (not color):
            if self.board[x][y-1] == color:
                return True
            if self.board[x][y-1] is NONE:
                return False
            if y == 1:
                return False
            y -= 1
        return False

    def check_ne(self,color,co):
        x = co[0]
        y = co[1]
        if x <= 1 or y >= 6:
            return False
        x -= 1
        y += 1
        while self.board[x][y] == (not color):
            if self.board[x-1][y+1] == color:
                return True
            if self.board[x-1][y+1] is NONE:
                return False
            if x == 1 or y == 6:
                return False
            x -= 1
            y += 1
        return False

    def check_se(self,color,co):
        x = co[0]
        y = co[1]
        if x >= 6 or y >= 6:
            return False
        x += 1
        y += 1
        while self.board[x][y] == (not color):
            if self.board[x+1][y+1] == color:
                return True
            if self.board[x+1][y+1] is NONE:
                return False
            if x == 6 or y == 6:
                return False
            x += 1
            y += 1
        return False

    def check_sw(self,color,co):
        x = co[0]
        y = co[1]
        if x >= 6 or y <= 1:
            return False
        x += 1
        y -= 1
        while self.board[x][y] == (not color):
            if self.board[x+1][y-1] == color:
                return True
            if self.board[x+1][y-1] is NONE:
                return False
            if x == 6 or y == 1:
                return False
            x += 1
            y -= 1
        return False

    def check_nw(self,color,co):
        x = co[0]
        y = co[1]
        if x <= 1 or y <= 1:
            return False
        x -= 1
        y -= 1
        while self.board[x][y] == (not color):
            if self.board[x-1][y-1] == color:
                return True
            if self.board[x-1][y-1] is NONE:
                return False
            if x == 1 or y == 1:
                return False
            x -= 1
            y -= 1
        return False



    def reverse_n(self,color,co):
        x = co[0]
        y = co[1]
        while True:
            x -= 1
            if self.board[x][y] == color:
                break
            self.board[x][y] = color
            self.reversed_list.append((x,y))

    def reverse_e(self,color,co):
        x = co[0]
        y = co[1]
        while True:
            y += 1
            if self.board[x][y] == color:
                break
            self.board[x][y] = color
            self.reversed_list.append((x,y))

    def reverse_s(self,color,co):
        x = co[0]
        y = co[1]
        while True:
            x += 1
            if self.board[x][y] == color:
                break
            self.board[x][y] = color
            self.reversed_list.append((x,y))

    def reverse_w(self,color,co):
        x = co[0]
        y = co[1]
        while True:
            y -= 1
            if self.board[x][y] == color:
                break
            self.board[x][y] = color
            self.reversed_list.append((x,y))

    def reverse_ne(self,color,co):
        x = co[0]
        y = co[1]
        while True:
            x -= 1
            y += 1
            if self.board[x][y] == color:
                break
            self.board[x][y] = color
            self.reversed_list.append((x,y))

    def reverse_se(self,color,co):
        x = co[0]
        y = co[1]
        while True:
            x += 1
            y += 1
            if self.board[x][y] == color:
                break
            self.board[x][y] = color
            self.reversed_list.append((x,y))

    def reverse_sw(self,color,co):
        x = co[0]
        y = co[1]
        while True:
            x += 1
            y -= 1
            if self.board[x][y] == color:
                break
            self.board[x][y] = color
            self.reversed_list.append((x,y))

    def reverse_nw(self,color,co):
        x = co[0]
        y = co[1]
        while True:
            x -= 1
            y -= 1
            if self.board[x][y] == color:
                break
            self.board[x][y] = color
            self.reversed_list.append((x,y))

    def check(self,color,co):
        return (self.check_n(color,co) or self.check_e(color,co) or self.check_s(color,co)\
               or self.check_w(color,co) or self.check_ne(color,co) or self.check_se(color,co)\
               or self.check_sw(color,co) or self.check_nw(color,co)) and (self.board[co[0]][co[1]] is NONE)

    def reverse(self,color,co):
        self.reversed_list = []
        self.board[co[0]][co[1]] = color
        if self.check_n(color,co):
            self.reverse_n(color,co)
        if self.check_e(color,co):
            self.reverse_e(color,co)
        if self.check_s(color,co):
            self.reverse_s(color,co)
        if self.check_w(color,co):
            self.reverse_w(color,co)
        if self.check_ne(color,co):
            self.reverse_ne(color,co)
        if self.check_se(color,co):
            self.reverse_se(color,co)
        if self.check_sw(color,co):
            self.reverse_sw(color,co)
        if self.check_nw(color,co):
            self.reverse_nw(color,co)
        self.co_record.append(co)
        self.color_record.append(color)
        self.reversed_record.append(self.reversed_list)

    def undo(self):
        for (x,y) in self.reversed_record.pop():
            self.board[x][y] = not self.board[x][y]
        (i,j) = self.co_record.pop()
        self.color_record.pop()
        self.board[i][j] = NONE 

    def check_gameover(self,color):
        for x,y in product(range(8),repeat=2):
            if self.check(not(color),(x,y)):
                break
        else:
            for x,y in product(range(8),repeat=2):
                if self.check(color,(x,y)):
                    break
            else:
                return GAMEOVER
            return PASS
        return NORMAL

    def put_stone(self,color,co):
        self.reverse(color,co)
        isgameover = self.check_gameover(color)
        if isgameover == GAMEOVER:
            return GAMEOVER
        elif isgameover == PASS:
            return PASS
        return NORMAL

    #undo_,undo_for_review,reverse_for_review GUI用
    def undo_(self):
        for (x,y) in self.reversed_record.pop():
            self.board[x][y] = not self.board[x][y]
        (i,j) = self.co_record.pop()
        color = self.board[i][j]
        self.color_record.pop()
        self.board[i][j] = NONE
        return color 
    
    def undo_for_review(self,pointer):
        for (x,y) in self.reversed_record[pointer]:
            self.board[x][y] = not self.board[x][y]
        (i,j) = self.co_record[pointer]
        self.board[i][j] = NONE

    def reverse_for_review(self,pointer):
        color = self.color_record[pointer]
        co = self.co_record[pointer]
        reversed_list = self.reversed_record[pointer]
        self.board[co[0]][co[1]] = color
        for co in reversed_list:
            self.board[co[0]][co[1]] = not self.board[co[0]][co[1]]
    

    def value_func(self):

        #デバッグ用
        #global count
        #count += 1


        value = 0
        value_map = ((30,-12,0,-1,-1,0,-12,30),
                     (-12,-15,-3,-3,-3,-3,-15,-12),
                     (0,-3,0,-1,-1,0,-3,0),
                     (-1,-3,-1,-1,-1,-1,-3,-1),
                     (-1,-3,-1,-1,-1,-1,-3,-1),
                     (0,-3,0,-1,-1,0,-3,0),
                     (-12,-15,-3,-3,-3,-3,-15,-12),
                     (30,-12,0,-1,-1,0,-12,30))
        black = 0
        white = 0
        for x,y in product(range(8),repeat=2):
            if self.board[x][y] == BLACK:
                value += value_map[x][y]
                black += 1
            elif self.board[x][y] == WHITE:
                value -= value_map[x][y]
                white += 1
            else:
                value += (0,3)[self.check(BLACK,(x,y))]
                value -= (0,3)[self.check(WHITE,(x,y))]
        if black + white >= 52:
            return black
        return value

    def count_stone(self):
        black = 0
        white = 0
        for (x,y) in product(range(8),repeat=2):
            if self.board[x][y] == BLACK:
                black += 1
            elif self.board[x][y] == WHITE:
                white += 1
        return black,white

    def print_board(self):
        print()
        for row in self.board:
            print("  ")
            for col in row:
                if col == BLACK:
                    print("○ ",end="")
                elif col == WHITE:
                    print("● ",end="")
                else:
                    print("   ",end="")
            print(" ")



MAX_VALUE = 10000
MIN_VALUE = -10000

def move_first(depth,b,limit):
    if depth == 0:
        return b.value_func(),[]
    value = MIN_VALUE
    move = []
    for x,y in product(range(8),repeat=2):
        if not b.check(BLACK,(x,y)):
            continue
        result = b.put_stone(BLACK,(x,y))
        m = []
        if result == GAMEOVER:
            v = b.value_func()
        elif result == PASS:
            v,m = move_first(depth,b,limit)
        else:
            v,_ = move_second(depth-1,b,value)
        if value < v:
            value = v
            move = [(x,y)] + m
        b.undo()
        if value >= limit:
            break
    return value,move

def move_second(depth,b,limit):
    if depth == 0:
        return b.value_func(),[]
    value = MAX_VALUE
    move = []
    for x,y in product(range(8),repeat=2):
        if not b.check(WHITE,(x,y)):
            continue
        result = b.put_stone(WHITE,(x,y))
        m = []
        if result == GAMEOVER:
            v = b.value_func()
        elif result == PASS:
            v,m = move_second(depth,b,limit)
        else:
            v,_ = move_first(depth-1,b,value)
        if value > v:
            value = v
            move = [(x,y)] + m
        b.undo()
        if value <= limit:
            break
    return value,move

def play(first_depth, second_depth):
    board = Board(BOARD)
    color = BLACK
    while True:
        if color == BLACK:
            value,move = move_first(first_depth, board,MAX_VALUE)
        else:
            value ,move = move_second(second_depth,board,MIN_VALUE)
        for x in move:
            print("move ",x)
            result = board.put_stone(color,x)
            board.print_board()
        if result == GAMEOVER:
            print("Game Over")
            print(board.count_stone())
            return None
        color = not color

#ミニマックス法の評価関数を後手の時のみマイナスにすることで自身の回帰で読める
def negamax(color,depth,b,limit):
    if depth == 0:
        v = b.value_func()
        if color == WHITE:
            v = -v
        return v,[]

    value = MIN_VALUE
    move = []
    for x,y in product(range(8),repeat=2):
        if not b.check(color,(x,y)):
            continue
        result = b.put_stone(color,(x,y))
        m = []
        if result == GAMEOVER:
            v = b.value_func()
            if color == WHITE:
                v = -v
        elif result == PASS:
            v,m = negamax(color,depth,b,limit)
        else:
            v,_ = negamax(not(color),depth-1,b,-value)
            v = -v
        if value < v:
            value = v
            move = [(x,y)] + m
        b.undo()
        if value >= limit:
            break
    return value,move


def play_negamax(first_depth, second_depth):
    board = Board(BOARD)
    color = BLACK
    while True:
        if color == BLACK:
            value,move = negamax(color,first_depth,board,MAX_VALUE)
        else:
            value,move = negamax(color,second_depth,board,MAX_VALUE)
        for x in move:
            print("move ",x)
            result = board.put_stone(color,x)
            board.print_board()
        if result == GAMEOVER:
            print("Game Over")
            print(board.count_stone())
            return None
        color = not color

def co_to_str(co):
    x = co[0]
    y = co[1]
    row = ["A","B","C","D","E","F","G","H"]
    col = ["1","2","3","4","5","6","7","8"]
    return row[y]+col[x]

def str_to_co(string):
    x = string[0]
    y = string[1]
    col = {"A"}
    return int(y)-1 , ord(x) - 65

def add_sign(n):
    if n > 0:
        return "+"+str(n)
    else:
        return str(n)

def double_padding(string,n):
    tmp = ""
    for _ in range(n-len(string)):
        tmp += "  "
    return tmp + string



if __name__ == "__main__":
    print(co_to_str((3,6)))
