import tkinter
import time
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
        self.bind("<1>",self.cur)

    def cur(self,event):
        self.after(1,cur2)
    def cur2(self):
        print(self.curselection()[0])


if __name__ == "__main__":
    window = tkinter.Tk()
    box = ScrolledListbox(master=window,selectmode="browse")
    box.pack()
    ais = ["STATIC VALUE FUNCTION","RANDOM VALUE FANCTION",
           "EX3","EX4","EX5","EX6","EX7","EX8","EX9","EX10"]
    box.insert(tkinter.END,*ais)
    box.select_set(1)
    window.mainloop()