from board import co_to_str,str_to_co,BLACK,WHITE
import datetime 

"""
datetime  (gameboard.date.strftime("%Y/%m/%d %H:%M:%S"))
                           ↑日付→文字列
                           strptime
                           文字列→日付()



ファイル形式kif utf-8

#comment
20XX/XX/XX XX:XX:XX 
B Player
W Player
28 36
1 B E6
2 W F5
3 ....
60 W A1
"""

class Record:
    def __init__(self,comment="#null",date=datetime.datetime.now(),black="null",
    white="null",black_stone="null",white_stone="null",
    color_record=[],co_record=[]):
        self.comment = comment 
        self.date = date
        self.black = black 
        self.white = white
        self.black_stone = black_stone
        self.white_stone = white_stone 
        self.color_record = color_record 
        self.co_record = co_record
    def read_record(self,stream):
        line = stream.readline()[:-1]
        if line[0] == "#":
            self.comment = line[1:]
            line = stream.readline()[:-2]
        self.date = datetime.datetime.strptime(line ,"%Y/%m/%d %H:%M:%S")
        line = stream.readline()[:-1]
        self.black = line.split(" ")[1]
        line = stream.readline()[:-1]
        self.white = line.split(" ")[1]
        line = stream.readline()[:-1]
        self.black_stone,self.white_stone = map(int,line.split(" "))
        
        self.color_record = []
        self.co_record = []
        line = stream.readline()[:-1].split()
        while line:
            self.color_record.append(symbol(line[1]))
            self.co_record.append(str_to_co(line[2]))
            line = stream.readline()[:-1].split()

    def write_record(self,stream):
        stream.write(self.comment +"\n")
        stream.write(self.date.strftime("%Y/%m/%d %H:%M:%S") + "\n")
        stream.write("B " + self.black + "\n")
        stream.write("W " + self.white + "\n")
        stream.write(str(self.black_stone) + " " + str(self.white_stone) + "\n")
        for i in range(len(self.color_record)):
            stream.write(str(i+1)+" "+("W","B")[self.color_record[i]]+" "+co_to_str(self.co_record[i])+"\n")
       


        

def symbol(string):
    if string == "B":
        return BLACK
    elif string == "W":
        return WHITE
    else:
        raise NameError

