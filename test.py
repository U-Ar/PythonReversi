import tkinter
from board import *
from functools import partial
import time
from copy import deepcopy


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

class GameOptionButton(tkinter.Button):
    def __init__(self,master=None):
        super(GameOptionButton,self).__init__(master=master,
        command=self.boot_gameoption,text="GAMESTART")
    
    def boot_gameoption(self):
        gameoption_window = tkinter.Tk()
        #セルフのマスターウィジェットを閉じる動作は
        #self.master.destroy()をメインループの前に実行
        #self.master=masterをすると逆効果
        self.master.destroy()
        gameoption_window.title("game option")
        gameoption = GameOption(gameoption_window)
        gameoption.pack()
        gameoption_window.mainloop()

class GameOption(tkinter.Frame):
    #対局の設定ボタンの配置　色、ステップ、評価関数について決定
    def __init__(self,master=None):
        super(GameOption,self).__init__(master=master)
        
        label1 = tkinter.Label(master=self,text="SELECT YOUR COLOR")
        label1.pack()

        self.colorvar = tkinter.BooleanVar(master=self)
        self.colorvar.set(BLACK)
        blackbutton = tkinter.Radiobutton(master=self,text="BLACK",variable=self.colorvar,value=BLACK)
        whitebutton = tkinter.Radiobutton(master=self,text="WHITE",variable=self.colorvar,value=WHITE)
        blackbutton.pack()
        whitebutton.pack()

        label2 = tkinter.Label(master=self,text="SELECT AI'S THINKING STEPS")
        label2.pack()
        
        self.stepsvar = tkinter.IntVar(master=self)
        self.stepsvar.set(1)
        self.aisteps = tkinter.Spinbox(master=self, from_ = 1, to = 7, increment = 1, width = 8, textvariable=self.stepsvar)
        self.aisteps.pack(fill="x")

        label3 = tkinter.Label(master=self,text="SELECT AI'S VALUE FUNCTION")
        label3.pack()

        self.ailist = tkinter.Listbox(master=self,selectmode="browse",height=3)
        self.ailist.pack(fill="x")
        ais = ["STATIC VALUE FUNCTION","RANDOM VALUE FANCTION"]
        self.ailist.insert(tkinter.END,*ais)
        self.ailist.select_set(0)

        start_button = GameBoardButton(self)
        start_button.pack()

class GameBoardButton(tkinter.Button):
    def __init__(self,master=None):
        super(GameBoardButton,self).__init__(master=master,
        command=self.boot_gameboard,text="GAME START")
    
    def boot_gameboard(self):
        selected_color = self.master.colorvar.get()
        selected_steps = self.master.aisteps.get()
        selected_ai = self.master.ailist.curselection()[0]
        
        gameboard_window = tkinter.Tk()
        gameboard_window.title("Playing")
        gameboard_window.geometry("600x400")
        gameboard_window.minsize(600,400)

        menubar = tkinter.Menu(gameboard_window)
        gameboard_window.configure(menu = menubar)
        gamemenu = tkinter.Menu(menubar, tearoff = False)
        optionmenu = tkinter.Menu(menubar, tearoff = False)
        menubar.add_cascade(label="Game", underline = 0, menu=gamemenu)
        menubar.add_cascade(label="Option", underline = 0, menu=optionmenu)
        
        #Gameメニューに置くメニュー群　NEW GAME  TITLE  QUIT
        bind_boot_gameoption = partial(boot_gameoption,gameboard_window)
        gamemenu.add_command(label = "New game", under = 0, command = bind_boot_gameoption)
        
        bind_boot_startmenu = partial(boot_startmenu,gameboard_window)
        gamemenu.add_command(label= "Back to Title",under=0, command = bind_boot_startmenu)
        
        _quit = lambda x: x.destroy()
        bind_quit = partial(_quit,gameboard_window)
        gamemenu.add_command(label="Quit",under=0,command=bind_quit)

        previous_step = tkinter.StringVar(master=gameboard_window)
        previous_step.set("START")

        #盤面のキャンバス
        gameboard_window.gameboard = GameBoard(gameboard_window,color=selected_color,steps=selected_steps,ai=selected_ai,text=previous_step)
        gameboard_window.gameboard.pack(side=tkinter.LEFT)
        
        gameboard_window.textframe = tkinter.Frame(gameboard_window)
        gameboard_window.textframe.pack()
        #gameboardのメソッドを必要とする待ったコマンドなので初期化の後に追加
        optionmenu.add_command(label="Revert to Last Move",command=gameboard_window.gameboard.undo)
        
        console1 = tkinter.Label(gameboard_window.textframe,
                                 text="VS. {} STEP {} ALGORITHM".format(selected_steps,("STATIC","RANDOM")[selected_ai]))
        console1.pack()
        
        self.console2 = tkinter.Label(gameboard_window.textframe,textvariable=previous_step)
        self.console2.pack()

        self.master.master.destroy()
        gameboard_window.mainloop()


class GameBoard(tkinter.Canvas):
    #masterのデフォルト値が設定されていないので使用の際は注意
    def __init__(self,master,color,steps,ai,text):
        #CanvasのクリックとBoardインスタンスのput_stoneを紐づけ
        self.color = color 
        self.steps = int(steps) 
        self.ai = ai
        self.previous_step = text

        self.grid_size = 40
        board_size = self.grid_size * 9

        super(GameBoard,self).__init__(master=master, relief=tkinter.RAISED, bd=4, bg="#008000",
                           width=10*self.grid_size, height=10*self.grid_size, highlightthickness=0)
        for i in range(9):
            x = (i+1) * self.grid_size
            self.create_line(x, self.grid_size, x, board_size)
            self.create_line(self.grid_size, x, board_size, x)

        self.bind("<1>",self.put_stone)
        self.board = Board(deepcopy(BOARD))
        self.render_board(BLACK)
        if self.color == WHITE:
            self.after(1000,self.ai_puts_stone)
            self.render_board(BLACK)
        self.enabled = True
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
                            self.boot_result()
                            
                        else:
                            self.render_board(self.color)
                            self.previous_step.set("Player's Move "+co_to_str((row,col))+"    Now AI's Turn")
                            self.after(1,self.ai_puts_stone)
        
    def ai_puts_stone(self):
        value,move = negamax(not(self.color),self.steps,self.board,(MIN_VALUE,MAX_VALUE)[self.color])
        for x in move:
            result = self.board.put_stone(not(self.color),x)
            self.render_board(not(self.color))
            if x != move[-1]:
                self.previous_step.set("AI's Move: "+co_to_str(x))
                time.sleep(0.5)
                self.previous_step.set("Player Passes")
            else:
                self.previous_step.set("AI's Move: "+co_to_str(x)+"    Now Player's Turn")
            
            

        self.render_board(self.color)

        if result == GAMEOVER:
            self.previous_step.set("GAMEOVER")
            self.boot_result()

        self.enabled = True
    
    def boot_result(self):
        time.sleep(1)
        result_window = tkinter.Toplevel()
        label4 = tkinter.Label(result_window,text="RESULT")
        label4.pack()
        black,white = self.board.count_stone()
        label5 = tkinter.Label(result_window,text="BLACK {} : WHITE {}".format(black,white))
        label5.pack()
        if black != white:
            result = ("YOU WIN","YOU LOSE")[self.color == (black<white)]
        else:
            result = "DRAW"
        label6 = tkinter.Label(result_window,text=result)
        label6.pack()
        
        reviewbutton = tkinter.Button(master=result_window,text="Review the game",
                                      command=partial(boot_review,self,result_window))
        reviewbutton.pack()
        bind_quit = partial(lambda x: x.destroy() ,self.master) 
        quitbutton = tkinter.Button(master=result_window,text="Quit the game",command=bind_quit)
        quitbutton.pack()

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
    
    def undo(self):
        color = not self.color
        while color != self.color:
            color = self.board.undo_()
        self.render_board(self.color)
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
        self.render_board(not self.color)

def record_to_p(window):
    window.record_list.selection_clear(window.pointer+1)
    window.pointer = -1
    window.board.board = deepcopy(BOARD)
    window.delete_highlight()
    window.render_board(not window.color)
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
    window.render_board(not window.color)
    window.record_list.selection_set(window.pointer+1)
    window.record_list.see(window.pointer+1)

def record_to_f(window):
    if window.pointer + 1 == len(window.board.co_record):
        return
    window.record_list.selection_clear(window.pointer+1)
    window.pointer += 1
    window.board.reverse_for_review(window.pointer)
    window.highlight_change()
    window.render_board(not window.color)
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
    window.render_board(not window.color)
    window.record_list.selection_set(window.pointer+1)
    window.record_list.see(window.pointer+1)

def click(gameboard,event):
    gameboard.record_list.after(1,gameboard.click_record)

def boot_review(gameboard,result_window):
    result_window.destroy()

    gameboard.previous_step.set("Review Mode  You: " + ["○","●"][gameboard.color])

    gameboard.pointer = len(gameboard.board.co_record) - 1
    gameboard.highlight_change()
    gameboard.render_board(not gameboard.color)
    
    gameboard.buttonframe = tkinter.Frame(gameboard.master)
    gameboard.buttonframe.pack(fill="both")
    gameboard.previousbutton = tkinter.Button(gameboard.buttonframe,text="<< ",command=partial(record_to_p,gameboard))
    gameboard.backbutton = tkinter.Button(gameboard.buttonframe,text=" < ",command=partial(record_to_b,gameboard))
    gameboard.forwardbutton = tkinter.Button(gameboard.buttonframe,text=" > ",command=partial(record_to_f,gameboard))
    gameboard.nextbutton = tkinter.Button(gameboard.buttonframe,text=" >>",command=partial(record_to_n,gameboard))
    gameboard.previousbutton.grid(column=0,row=0)
    gameboard.backbutton.grid(column=1,row=0)
    gameboard.forwardbutton.grid(column=2,row=0)
    gameboard.nextbutton.grid(column=3,row=0)

    co_record = list(map(co_to_str,gameboard.board.co_record))
    color_record = list(map(lambda x: ["○ ","● "][x] ,gameboard.board.color_record))
    record = [" "]
    for i,co,color in zip(range(len(co_record)),co_record,color_record):
        record.append(str(i+1).rjust(3) +": "+color+co)
    gameboard.record_list = ScrolledListbox(master=gameboard.master,
                                            height=21,
                                            selectmode="browse",
                                            selectbackground="LightBlue",
                                            selectforeground="black"
                                            )
    gameboard.record_list.pack(fill=tkinter.BOTH)
    gameboard.record_list.insert(tkinter.END,*record)
    gameboard.record_list.selection_set(gameboard.pointer+1)
    gameboard.record_list.see(gameboard.pointer+1)
    gameboard.record_list.bind("<1>", partial(click, gameboard))

def boot_gameoption(current_window):
    gameoption_window = tkinter.Tk()
    gameoption_window.geometry("200x300")
    current_window.destroy()
    gameoption_window.title("game option")
    gameoption = GameOption(gameoption_window)
    gameoption.pack()
    gameoption_window.mainloop()

def boot_startmenu(current_window):
    startmenu = tkinter.Tk()
    startmenu.geometry("200x200")
    startmenu.title("startmenu")
    
    start_label = tkinter.Label(startmenu,text="Reversi PYTHON DRIVEN EDITION")
    start_label.pack()
    new_game = GameOptionButton(startmenu)
    new_game.pack(fill=tkinter.BOTH)

    quit_button = tkinter.Button(startmenu,text="quit",command=startmenu.destroy)
    quit_button.pack(fill=tkinter.BOTH)

    if current_window != None:
        current_window.destroy()
    startmenu.mainloop()

if __name__ == "__main__":
    boot_startmenu(None)