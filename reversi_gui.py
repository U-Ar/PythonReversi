import tkinter 
from board import *

YOUR_COLORS = {"black":True, "white":False}


top = tkinter.Tk()



class GUIGameBoard(tkinter.Canvas):




    def __init__(self, master, your_color):
        self.grid_size = 50
        en = self.grid_size * 9
        z = self.grid_size * 0.36
        self.master = master

        tkinter.Canvas.__init__(self, master, relief=tkinter.RAISED, bd=4, bg="#008000",
                           width=10*self.grid_size, height=10*self.grid_size, highlightthickness=0)


        self.bind("<1>", self.put_stone)
        for i in range(9):
            x = (i+1) * self.grid_size
            self.create_line(x, self.grid_size, x, en)
            self.create_line(self.grid_size, x, en, x)

        for j in range(8):
            x = (j+1) * self.grid_size
            self.create_text(z, x+self.grid_size/2, text=str(j+1), justify=tkinter.RIGHT, fill="#002010",
                              font=("Helvetica","12","normal"))
            self.create_text(x+self.grid_size/2, z, text=str(j+1), justify=tkinter.CENTER, fill="#002010",
                              font=("Helvetica","12","normal"))

        self.your_color = your_color
        self.color = BLACK

        self.b = Board(BOARD)

        if self.your_color == WHITE:
            self.game.ai_puts_stone(BLACK)

        self.render_player_side()

        self.enabled = True



    def render(self):
        self.delete("stone")
        for x in range(8):
            for y in range(8):
                if self.b.board[x][y] != None:
                    r = self.grid_size * 0.45
                    x_left = (y+1.5)*self.grid_size - r
                    x_right = (y+1.5)*self.grid_size + r
                    y_top = (x+1.5)*self.grid_size-r
                    y_bottom = (x+1.5)*self.grid_size+r
                    self.create_oval(x_left, y_top, x_right, y_bottom, fill = ["white","black"][self.b.board[x][y]], tags = "stone")

    def render_player_side(self):
        self.delete("stone")
        for x in range(8):
            for y in range(8):
                if self.b.board[x][y] != None:
                    r = self.grid_size * 0.45
                    x_left = (y+1.5)*self.grid_size - r
                    x_right = (y+1.5)*self.grid_size + r
                    y_top = (x+1.5)*self.grid_size-r
                    y_bottom = (x+1.5)*self.grid_size+r
                    self.create_oval(x_left, y_top, x_right, y_bottom, fill = ["white","black"][self.b.board[x][y]], tags = "stone")
                else:
                    if self.b.check(self.your_color,(x,y)):
                        r = self.grid_size * 0.45
                        x_left = (y+1.5)*self.grid_size - r
                        x_right = (y+1.5)*self.grid_size + r
                        y_top = (x+1.5)*self.grid_size-r
                        y_bottom = (x+1.5)*self.grid_size+r
                        self.create_rectangle(x_left, y_top, x_right, y_bottom, activefill="#32CD32", width=0, tags = "stone")

    def put_stone(self, event):
        cx = self.canvasx(event.x)
        cy = self.canvasy(event.y)
        col = int(cx//self.grid_size) - 1
        row = int(cy//self.grid_size) - 1
        if self.enabled:
            if (0<=row<=7 and 0<=col<=7):
                if (self.b.board[row][col]) == None:
                    if self.b.check(self.your_color,(row, col)):
                        self.enabled = False
                        result = self.b.put_stone(self.your_color,(row,col))
                        self.master.echo.set("")
                        if result == PASS:
                            self.master.echo.set("AI passes")
                            self.render_player_side()
                            self.enabled = True
                        elif result == GAMEOVER:
                            self.render()
                            black,white = self.b.count_stone()
                            self.master.echo.set("Game Over" +" %2d : %2d" %(black,white))
                        else:
                            self.render()
                            self.after(1,self.ai_puts_stone)

    def ai_puts_stone(self):
        value,move = negamax(not(self.your_color),5,self.b,MAX_VALUE)
        for x in move:
            result = self.b.put_stone(not(self.your_color),x)
            self.render()

        self.render_player_side()

        print(self.b.value_func())

        if result == GAMEOVER:
            black,white = self.b.count_stone()
            self.master.echo.set("Game Over" +" %2d : %2d" %(black,white))
        self.enabled = True





class GUIFrame(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.master.title("Reversi")
        self.echo = tkinter.StringVar()





        l_title = tkinter.Label(self, text="Reversi", font=("Times","24",("italic","bold")),
                           fg="#191970", bg="#008000", width=12)
        l_title.pack(padx=10,pady=10)

        self.reversi_board = GUIGameBoard(self, BLACK)

        self.reversi_board.pack(padx=10,pady=10)

        self.f_footer = tkinter.Frame(self)
        self.f_footer.pack()
        self.pass_indicator = tkinter.Label(self.f_footer,textvariable=self.echo, width=20, font=("Times", "12"))
        self.pass_indicator.pack(side=tkinter.LEFT, padx=5, pady=5)
        self.reset_button = tkinter.Button(self.f_footer, text="reset", font=("Times", 14), command=self.reset)
        self.reset_button.pack(side=tkinter.RIGHT, padx=5, pady=5)

    def reset(self):
        pass







if __name__ == "__main__":
    f = GUIFrame(None)
    f.pack()
    f.mainloop()
