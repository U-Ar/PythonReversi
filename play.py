import tkinter
from tkinter import filedialog
from board import *
from record import *
from bitoperations import bit_negamax,co_to_bit,bit_to_co,board_to_bit,value_func_static,value_func_random
from functools import partial
import time
from copy import deepcopy
import sys,os
import datetime

FILETYPES = [("Record",("kif",))]
FUNCS = [value_func_static,value_func_random]


class ScrolledListbox(tkinter.Listbox):
    def __init__(self,master,**key):
        self.frame = tkinter.Frame(master)
        self.yscroll = tkinter.Scrollbar(self.frame,orient=tkinter.VERTICAL)
        self.yscroll.pack(side=tkinter.RIGHT,fill=tkinter.Y,expand=1)
        key["yscrollcommand"] = self.yscroll.set
        super().__init__(master=self.frame,**key)
        self.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=1)
        self.yscroll.config(command=self.yview)

        for m in (list(tkinter.Pack.__dict__.keys()) + list(tkinter.Grid.__dict__.keys()) \
                   + list(tkinter.Place.__dict__.keys())):
            m[0] == "_" or m == "config" or m == "configure" or \
                setattr(self,m,getattr(self.frame,m))

class GameBoard(tkinter.Canvas):
    def __init__(self,master):
        #color.steps.ai.textをゲーム開始時に受け取る必要あり
        #self.color = color 
        #self.steps = int(steps) 
        #self.ai = ai
        #self.previous_step = text

        self.grid_size = 40
        board_size = self.grid_size * 9

        super(GameBoard,self).__init__(master=master, relief=tkinter.RAISED, bd=4, bg="#008000",
                           width=10*self.grid_size, height=10*self.grid_size, highlightthickness=0)
        for i in range(9):
            x = (i+1) * self.grid_size
            self.create_line(x, self.grid_size, x, board_size)
            self.create_line(self.grid_size, x, board_size, x)

        self.bind("<1>",self.put_stone)
        #enabledをFalseに、起動時にTrueにする必要
        self.enabled= False
        
        self.board = Board(deepcopy(BOARD))

        self.pointer = 0

    def put_stone(self,event):
        cx = self.canvasx(event.x)
        cy = self.canvasy(event.y)
        col = int(cx//self.grid_size) - 1
        row = int(cy//self.grid_size) - 1
        if self.enabled:
            if (0<=row<=7 and 0<=col<=7):
                if (self.board.board[row][col]) == None:
                    if self.board.check(self.color,(row, col)):
                        self.enabled = False
                        result = self.board.put_stone(self.color,(row,col))
                        if result == PASS:
                            self.render_board(self.color)
                            self.previous_step.set("Player's Move "+co_to_str((row,col)))
                            time.sleep(0.5)
                            self.previous_step.set("AI Passes")
                            self.enabled = True
                        elif result == GAMEOVER:
                            self.render_board(self.color)
                            self.previous_step.set("GAME OVER")
                            boot_result(self)
                            
                        else:
                            self.render_board(self.color)
                            self.previous_step.set("Player's Move "+co_to_str((row,col))+"    Now AI's Turn")
                            self.after(1,self.ai_puts_stone)
        
    def ai_puts_stone(self):
        """
        _,move = negamax(not(self.color),self.steps,self.board,(MIN_VALUE,MAX_VALUE)[self.color])
        for x in move:
            result = self.board.put_stone(not(self.color),x)
            self.render_board(not(self.color))
            if x != move[-1]:
                self.previous_step.set("AI's Move: "+co_to_str(x))
                time.sleep(0.5)
                self.previous_step.set("Player Passes")
            else:
                self.previous_step.set("AI's Move: "+co_to_str(x)+"    Now Player's Turn")
        """
        if self.color == BLACK:
            white,black = board_to_bit(self.board.board)
        else:
            black,white = board_to_bit(self.board.board)
        _,move,__ = bit_negamax(black,white,self.steps,MIN_VALUE,MAX_VALUE,False,self.func)
        for m in move:
            result = self.board.put_stone(not(self.color),bit_to_co(m))
            self.render_board(not(self.color))
            if m != move[-1]:
                self.previous_step.set("AI's Move: "+co_to_str(bit_to_co(m)))
                time.sleep(0.2)
                self.previous_step.set("Player Passes")
            else:
                self.previous_step.set("AI's Move: "+co_to_str(bit_to_co(m))+"    Now Player's Turn")
                self.render_board(self.color)
        
        if result == GAMEOVER:
            self.previous_step.set("GAMEOVER")
            boot_result(self)

        self.enabled = True

    def render_board(self,color):
        #colorの値に基づく分岐処理はオプション選択可能にする予定
        self.delete("stone")
        if color == self.color:
            for x in range(8):
                for y in range(8):
                    if self.board.board[x][y] != None:
                        r = self.grid_size * 0.45
                        x_left = (y+1.5)*self.grid_size - r
                        x_right = (y+1.5)*self.grid_size + r
                        y_top = (x+1.5)*self.grid_size-r
                        y_bottom = (x+1.5)*self.grid_size+r
                        self.create_oval(x_left, y_top, x_right, y_bottom,
                         fill = ("white","black")[self.board.board[x][y]], tags = "stone")
                    else:
                        if self.board.check(self.color,(x,y)):
                            r = self.grid_size * 0.45
                            x_left = (y+1.5)*self.grid_size - r
                            x_right = (y+1.5)*self.grid_size + r
                            y_top = (x+1.5)*self.grid_size-r
                            y_bottom = (x+1.5)*self.grid_size+r
                            self.create_rectangle(x_left, y_top, x_right, y_bottom, 
                            activefill="#32CD32", width=0, tags = "stone")
        else:
            self.render()
    
    def render(self):
        self.delete("stone")
        for x in range(8):
            for y in range(8):
                if self.board.board[x][y] != None:
                    r = self.grid_size * 0.45
                    x_left = (y+1.5)*self.grid_size - r
                    x_right = (y+1.5)*self.grid_size + r
                    y_top = (x+1.5)*self.grid_size-r
                    y_bottom = (x+1.5)*self.grid_size+r
                    self.create_oval(x_left, y_top, x_right, y_bottom, 
                    fill = ("white","black")[self.board.board[x][y]], tags = "stone")
    
    def highlight(self,x,y):
        self.delete("highlight")
        r = self.grid_size * 0.47
        x_left = (y+1.5)*self.grid_size - r
        x_right = (y+1.5)*self.grid_size + r
        y_top = (x+1.5)*self.grid_size-r
        y_bottom = (x+1.5)*self.grid_size+r
        self.create_rectangle(x_left, y_top, x_right, y_bottom,fill="LightGreen",width=0,tags="highlight")
    def delete_highlight(self):
        self.delete("highlight")
    def highlight_change(self):
        self.delete_highlight()
        co = self.board.co_record[self.pointer]
        self.highlight(co[0],co[1])
    def clear_board(self):
        self.delete("stone")
        self.delete("highlight")
    
    def undo(self):
        if len(self.board.co_record) == 0:
            return
        color = not self.color
        while color != self.color:
            color = self.board.undo_()
        self.render_board(self.color)
        if len(self.board.co_record) == 0:
            self.previous_step.set("Start ")
            return
        self.previous_step.set("AI's Move: "+co_to_str(self.board.co_record[-1])+"    Now Player's Turn")

    def click_record(self):
        clicked = self.record_list.curselection()[0]
        if clicked == 0:
            self.board.board = deepcopy(BOARD)
            self.delete_highlight()
            self.pointer = -1
        elif clicked < self.pointer + 1:
            while clicked < self.pointer + 1:
                self.board.undo_for_review(self.pointer)
                self.pointer -= 1
            self.highlight_change()
        elif clicked > self.pointer:
            while clicked - 1 > self.pointer:
                self.pointer += 1
                self.board.reverse_for_review(self.pointer)
            self.highlight_change()
        self.render()

def record_to_p(window):
    window.record_list.selection_clear(window.pointer+1)
    window.pointer = -1
    window.board.board = deepcopy(BOARD)
    window.delete_highlight()
    window.render()
    window.record_list.selection_set(0)
    window.record_list.see(0)

def record_to_b(window):
    if window.pointer == -1:
        return
    window.record_list.selection_clear(window.pointer+1)
    window.board.undo_for_review(window.pointer)
    window.pointer -= 1
    if window.pointer != -1:
        window.highlight_change()
    else:
        window.delete_highlight()
    window.render()
    window.record_list.selection_set(window.pointer+1)
    window.record_list.see(window.pointer+1)

def record_to_f(window):
    if window.pointer + 1 == len(window.board.co_record):
        return
    window.record_list.selection_clear(window.pointer+1)
    window.pointer += 1
    window.board.reverse_for_review(window.pointer)
    window.highlight_change()
    window.render()
    window.record_list.selection_set(window.pointer+1)
    window.record_list.see(window.pointer+1)

def record_to_n(window):
    if window.pointer + 1 == len(window.board.co_record):
        return
    window.record_list.selection_clear(window.pointer+1)
    for _ in range(window.pointer+1,len(window.board.co_record)):
        window.pointer += 1
        window.board.reverse_for_review(window.pointer)
    window.pointer = len(window.board.co_record) - 1
    window.highlight_change()
    window.render()
    window.record_list.selection_set(window.pointer+1)
    window.record_list.see(window.pointer+1)

def click(gameboard,event):
    gameboard.record_list.after(1,gameboard.click_record)



def save_record(gameboard):
    black = ("AI","Player")[gameboard.color] 
    white = ("Player","AI")[gameboard.color]
    record = Record(comment="#"+gameboard.vstext,
                    date = gameboard.date,
                    black = black,
                    white = white,
                    black_stone = gameboard.black_stone,
                    white_stone = gameboard.white_stone,
                    color_record = gameboard.board.color_record,
                    co_record = gameboard.board.co_record)    
    path = os.getcwd()
    filename = filedialog.asksaveasfilename(filetypes=FILETYPES,
                initialdir = path + "\\record",
                defaultextension=".kif",
                initialfile = gameboard.date.strftime("%Y_%m_%d_%H_%M_%S"),
                title="Saving the record")
    with open(filename,mode="w",encoding="utf-8") as f:
        record.write_record(f)


def boot_record(gameboard):
    #まるで対局直後かのような状態へ
    record = Record()
    path = os.getcwd()
    filename = filedialog.askopenfilename(filetypes = FILETYPES,
                initialdir = path + "\\record",
                defaultextension=".kif",
                title="Opening records")
    with open(filename,mode="r",encoding="utf-8") as f:
        record.read_record(f)
    gameboard.board.initialize(deepcopy(BOARD))
    value_record = []
    for color,co in zip(record.color_record,record.co_record):
        gameboard.board.put_stone(color,co)
        value_record.append(gameboard.board.value_func())
    gameboard.master.title("review")
    gameboard.ui.destroy()
    gameboard.ui = tkinter.Frame(gameboard.master)
    gameboard.ui.pack(fill="both")
    
    label0 = tkinter.Label(gameboard.ui,text="Date: "+record.date.strftime("%Y/%m/%d %H:%M:%S"))
    label0.pack()
    label1 = tkinter.Label(gameboard.ui,text=record.comment)
    label1.pack()
    label2 = tkinter.Label(gameboard.ui,text="●:  "+str(record.black_stone)+"    ○:  "+str(record.white_stone))
    label2.pack()
    label3 = tkinter.Label(gameboard.ui,text="●:  "+record.black+"    ○:  "+record.white)
    label3.pack()

    gameboard.pointer = -1
    gameboard.board.board = deepcopy(BOARD)
    gameboard.clear_board()
    gameboard.render()
    
    gameboard.buttonframe = tkinter.Frame(gameboard.ui)
    gameboard.buttonframe.pack(fill="both")
    width = 5
    gameboard.previousbutton = tkinter.Button(gameboard.buttonframe,text="  <<  ",width=width,command=partial(record_to_p,gameboard))
    gameboard.backbutton = tkinter.Button(gameboard.buttonframe,text="   <  ",width=width,command=partial(record_to_b,gameboard))
    gameboard.forwardbutton = tkinter.Button(gameboard.buttonframe,text="  >   ",width=width,command=partial(record_to_f,gameboard))
    gameboard.nextbutton = tkinter.Button(gameboard.buttonframe,text="  >>  ",width=width,command=partial(record_to_n,gameboard))
    gameboard.previousbutton.grid(column=0,row=0)
    gameboard.backbutton.grid(column=1,row=0)
    gameboard.forwardbutton.grid(column=2,row=0)
    gameboard.nextbutton.grid(column=3,row=0)

    co_record = list(map(co_to_str,gameboard.board.co_record))
    color_record = list(map(lambda x: ["○ ","● "][x] ,gameboard.board.color_record))
    gameboard.board.board = deepcopy(BOARD)
    record = [" "]
    for i,co,color,value in zip(range(len(co_record)),co_record,color_record,value_record):
        record.append(double_padding(str(i+1),3) +": "+color+co+"   "+double_padding(str(value),13))
    gameboard.record_list = ScrolledListbox(master=gameboard.ui,
                                            height=18,
                                            selectmode="browse",
                                            selectbackground="LightBlue",
                                            selectforeground="black"
                                            )
    gameboard.record_list.pack(fill=tkinter.BOTH)
    gameboard.record_list.insert(tkinter.END,*record)
    gameboard.record_list.selection_set(gameboard.pointer+1)
    gameboard.record_list.see(gameboard.pointer+1)
    gameboard.record_list.bind("<1>", partial(click, gameboard))


def boot_review(gameboard):
    gameboard.master.title("review")
    gameboard.ui.destroy()
    gameboard.ui = tkinter.Frame(gameboard.master)
    gameboard.ui.pack(fill="both")

    label1 = tkinter.Label(gameboard.ui,text=gameboard.vstext)
    label1.pack()

    label2 = tkinter.Label(gameboard.ui,text=gameboard.resulttext)
    label2.pack()

    gameboard.previous_step.set("Review Mode    You: " + ["○","●"][gameboard.color])
    gameboard.caption = tkinter.Label(gameboard.ui,textvariable=gameboard.previous_step)
    gameboard.caption.pack()

    gameboard.pointer = len(gameboard.board.co_record) - 1
    gameboard.highlight_change()
    gameboard.render()
    
    gameboard.buttonframe = tkinter.Frame(gameboard.ui)
    gameboard.buttonframe.pack(fill="both")
    width = 5
    gameboard.previousbutton = tkinter.Button(gameboard.buttonframe,text="  <<  ",width=width,command=partial(record_to_p,gameboard))
    gameboard.backbutton = tkinter.Button(gameboard.buttonframe,text="   <  ",width=width,command=partial(record_to_b,gameboard))
    gameboard.forwardbutton = tkinter.Button(gameboard.buttonframe,text="  >   ",width=width,command=partial(record_to_f,gameboard))
    gameboard.nextbutton = tkinter.Button(gameboard.buttonframe,text="  >>  ",width=width,command=partial(record_to_n,gameboard))
    gameboard.previousbutton.grid(column=0,row=0)
    gameboard.backbutton.grid(column=1,row=0)
    gameboard.forwardbutton.grid(column=2,row=0)
    gameboard.nextbutton.grid(column=3,row=0)

    co_record = list(map(co_to_str,gameboard.board.co_record))
    color_record = list(map(lambda x: ["○ ","● "][x] ,gameboard.board.color_record))
    value_record = []
    gameboard.board.board = deepcopy(BOARD)
    for i in range(0,gameboard.pointer+1):
        gameboard.board.reverse_for_review(i)
        value_record.append(add_sign(gameboard.board.value_func()))
    record = [" "]
    for i,co,color,value in zip(range(len(co_record)),co_record,color_record,value_record):
        record.append(double_padding(str(i+1),3) +": "+color+co+"   "+double_padding(value,13))
    gameboard.record_list = ScrolledListbox(master=gameboard.ui,
                                            height=18,
                                            selectmode="browse",
                                            selectbackground="LightBlue",
                                            selectforeground="black"
                                            )
    gameboard.record_list.pack(fill=tkinter.BOTH)
    gameboard.record_list.insert(tkinter.END,*record)
    gameboard.record_list.selection_set(gameboard.pointer+1)
    gameboard.record_list.see(gameboard.pointer+1)
    gameboard.record_list.bind("<1>", partial(click, gameboard))

    savebutton = tkinter.Button(gameboard.ui,text="Save the game",command=partial(save_record,gameboard))
    savebutton.pack(fill="both")

def boot_result(gameboard):
    gameboard.master.title("result")
    gameboard.optionmenu.entryconfig(0,state=tkinter.DISABLED) 
    time.sleep(1)
    gameboard.ui.destroy()
    gameboard.ui = tkinter.Frame(gameboard.master)
    gameboard.ui.pack(fill="both")
    label4 = tkinter.Label(gameboard.ui,text="RESULT")
    label4.pack()
    gameboard.black_stone,gameboard.white_stone = gameboard.board.count_stone()
    gameboard.resulttext = " ●    {} :  ○    {}".format(gameboard.black_stone,gameboard.white_stone)
    label5 = tkinter.Label(gameboard.ui,text=gameboard.resulttext)
    label5.pack() 
    if gameboard.black_stone != gameboard.white_stone:
        result = ("YOU WIN","YOU LOSE")[gameboard.color == (gameboard.black_stone<gameboard.white_stone)]
    else:
        result = "DRAW"
    label6 = tkinter.Label(gameboard.ui,text=result)
    label6.pack()
        
    reviewbutton = tkinter.Button(master=gameboard.ui,text="Review the game",
                                      command=partial(boot_review,gameboard))
    reviewbutton.pack(fill="both")
    quitbutton = tkinter.Button(master=gameboard.ui,text="Quit the game",command=gameboard.master.destroy)
    quitbutton.pack(fill="both")

def boot_gameoption(gameboard):
    gameboard.ui.destroy()
    gameboard.clear_board()
    gameboard.board.initialize(deepcopy(BOARD))
    gameboard.master.title("game option")

    gameboard.ui = tkinter.Frame(gameboard.master)
    gameboard.ui.pack(fill="both")
    label0 = tkinter.Label(gameboard.ui,text="Game Option")
    label0.pack()
    label1 = tkinter.Label(gameboard.ui,text="Select Your Color")
    label1.pack()

    gameboard.colorvar = tkinter.BooleanVar(master=gameboard)
    gameboard.colorvar.set(BLACK)
    blackbutton = tkinter.Radiobutton(gameboard.ui,text="BLACK",variable=gameboard.colorvar,value=BLACK)
    whitebutton = tkinter.Radiobutton(gameboard.ui,text="WHITE",variable=gameboard.colorvar,value=WHITE)
    blackbutton.pack()
    whitebutton.pack()

    label2 = tkinter.Label(gameboard.ui,text="Select AI's Thinking Steps")
    label2.pack()
        
    gameboard.stepsvar = tkinter.IntVar(gameboard)
    gameboard.stepsvar.set(7)
    gameboard.aisteps = tkinter.Spinbox(gameboard.ui, 
    from_ = 1, to = 10, increment = 1, width = 8, textvariable=gameboard.stepsvar)
    gameboard.aisteps.pack(fill="x")

    label3 = tkinter.Label(gameboard.ui,text="Select AI's Value Function")
    label3.pack()

    gameboard.ailist = tkinter.Listbox(gameboard.ui,selectmode="browse",height=3)
    gameboard.ailist.pack(fill="x")
    ais = ["STATIC VALUE FUNCTION","RANDOM VALUE FANCTION"]
    gameboard.ailist.insert(tkinter.END,*ais)
    gameboard.ailist.select_set(0)

    start_button = tkinter.Button(gameboard.ui,text="Start The Game",command=partial(boot_game,gameboard))
    start_button.pack(fill="both")
    
def boot_game(gameboard):
    gameboard.master.title("playing")
    gameboard.date = datetime.datetime.now()
    gameboard.color = gameboard.colorvar.get() 
    gameboard.steps = int(gameboard.stepsvar.get()) 
    gameboard.ai = gameboard.ailist.curselection()[0]
    gameboard.func = FUNCS[gameboard.ai]
    gameboard.ui.destroy()

    gameboard.ui = tkinter.Frame(gameboard.master)
    gameboard.ui.pack(fill="both")
    
    console1 = tkinter.Label(gameboard.ui,
                                 text="VS. {} STEP {} ALGORITHM".format(gameboard.steps,("STATIC","RANDOM")[gameboard.ai]))
    gameboard.vstext = "VS. {} STEP {} ALGORITHM".format(gameboard.steps,("STATIC","RANDOM")[gameboard.ai])
    console1.pack()
    gameboard.console2 = tkinter.Label(gameboard.ui,textvariable=gameboard.previous_step)
    gameboard.console2.pack()

    gameboard.board = Board(deepcopy(BOARD))
    gameboard.render_board(BLACK)
    if gameboard.color == WHITE:
        gameboard.after(1000,gameboard.ai_puts_stone)
        gameboard.render_board(BLACK)
    gameboard.enabled=True
    gameboard.optionmenu.entryconfig(0,state=tkinter.NORMAL) 
    
def boot_start(gameboard):
    gameboard.ui.destroy()
    gameboard.optionmenu.entryconfig(0,state=tkinter.DISABLED)
    gameboard.clear_board()
    gameboard.board.initialize(deepcopy(BOARD))
    gameboard.ui = tkinter.Frame(gameboard.master)
    gameboard.ui.pack(fill="both")   
    start_label = tkinter.Label(gameboard.ui,text="Reversi PYTHON DRIVEN EDITION")
    start_label.pack()
    new_game = tkinter.Button(gameboard.ui,text="New Game",command=partial(boot_gameoption,gameboard))
    new_game.pack(fill=tkinter.BOTH)
    quit_button = tkinter.Button(gameboard.ui,text="quit",command=gameboard.master.destroy)
    quit_button.pack(fill=tkinter.BOTH)

def boot_startmenu():
    root = tkinter.Tk()
    root.geometry("600x400")
    root.title("Reversi")
    root.minsize(600,400)
    """
    start_label = tkinter.Label(startmenu,text="Reversi PYTHON DRIVEN EDITION")
    start_label.pack()
    new_game = GameOptionButton(startmenu)
    new_game.pack(fill=tkinter.BOTH)

    quit_button = tkinter.Button(startmenu,text="quit",command=startmenu.destroy)
    quit_button.pack(fill=tkinter.BOTH)

    if current_window != None:
        current_window.destroy()
    startmenu.mainloop()
    """
    gameboard = GameBoard(root)
    gameboard.pack(side="left")

    menubar = tkinter.Menu(root)
    root.configure(menu = menubar)
    gamemenu = tkinter.Menu(menubar, tearoff = False)
    gameboard.optionmenu = tkinter.Menu(menubar, tearoff = False)
    menubar.add_cascade(label="Game", underline = 0, menu=gamemenu)
    menubar.add_cascade(label="Option", underline = 0, menu=gameboard.optionmenu)
        
    #Gameメニューに置くメニュー群　NEW GAME  TITLE  QUIT
    bind_boot_gameoption = partial(boot_gameoption,gameboard)
    gamemenu.add_command(label = "New game", under = 0, command = bind_boot_gameoption)
    bind_boot_start = partial(boot_start,gameboard)
    gamemenu.add_command(label= "Back to Title",under=0, command = bind_boot_start)
    gamemenu.add_command(label= "Review records", under=0,command= partial(boot_record,gameboard))
    gamemenu.add_command(label= "Quit",under=0,command=root.destroy)
    
    gameboard.previous_step = tkinter.StringVar(master=gameboard)
    gameboard.previous_step.set("START")
        
    gameboard.ui = tkinter.Frame(root)
    gameboard.ui.pack(fill="both")
    gameboard.optionmenu.add_command(label="Revert to Last Move",command=gameboard.undo)
    gameboard.optionmenu.entryconfig(0,state=tkinter.DISABLED)    

    start_label = tkinter.Label(gameboard.ui,text="Reversi PYTHON DRIVEN EDITION")
    start_label.pack()
    new_game = tkinter.Button(gameboard.ui,text="New Game",command=partial(boot_gameoption,gameboard))
    new_game.pack(fill=tkinter.BOTH)

    quit_button = tkinter.Button(gameboard.ui,text="quit",command=root.destroy)
    quit_button.pack(fill=tkinter.BOTH)

    """
    console1 = tkinter.Label(gameboard_window,
                                 text="VS. {} STEP {} ALGORITHM".format(selected_steps,("STATIC","RANDOM")[selected_ai]))
    console1.pack()
        
    self.console2 = tkinter.Label(gameboard_window.textframe,textvariable=previous_step)
    self.console2.pack()
   """
    root.mainloop()

if __name__ == "__main__":
    boot_startmenu()