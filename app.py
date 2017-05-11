from tkinter import *
import tkinter.filedialog as fd
import os
from sys import *
import platform

fn = "Untitled"
pname = "Untitled"

def spaces(s):
    i = 0
    num = 0
    while(i<s):
        num += 8
        i+=1
    return str(num)

class MainApplication():
    def run(self, event):
        global fn
        if platform.system() == "Windows":
            os.system("python "+fn)
        else:
            os.system("python3 "+fn)
    def save(self, event):
        global fn
        if fn != "Untitled":
            f = open(fn, "w")
            f.write(self.text.get(0.0, END).rstrip())
            f.close()
        else:
            self.saveAs()
    def saveAs(self, event):
        global fn
        global pname

        fn = fd.asksaveasfilename(title="Save As", filetypes=(("Python Files", "*.py"), ("Python Files", "*.pyw")))
        pname = fn.split("/")
        pname = pname[len(pname)-1]
        self.root.title("Pedit - "+pname)
        self.save("")
    def __screen(self, event):
        self.text.width = event.width
        self.text.heigth = event.height
    def highlight(self,seq,bg,fg, font):
        #remove highlights
        self.highlights += 1
        if "highlight" in self.text.tag_names():
            content = self.text
            self.text.tag_delete(content,"highlight"+str(self.highlights))
        i = len(seq)
        index = "1.0"
        while True:
            index = self.text.search(seq, index, nocase=1, stopindex='end')
            if index:
                index2 = self.text.index("%s+%dc" % (index, i))
                self.text.tag_add('highlight'+str(self.highlights), index, index2)
                if font == "":
                    self.text.tag_configure('highlight'+str(self.highlights), background=bg, foreground=fg)
                else:
                    self.text.tag_configure('highlight'+str(self.highlights), font=font, background=bg, foreground=fg)
                index = index2
            else:
                return
    def __init__(self, title):
        self.highlights = 0
        self.root = Tk() # Declaring the tkinter window
        self.root.minsize(600,500)
        global pname
        self.root.title(title+" - "+pname)

        # Root Bindings
        self.root.bind("<Configure>", self.__screen)
        self.root.bind("<Control-o>", self.openf)
        self.root.bind("<Control-s>", self.save)
        self.root.bind("<Control-Shift-s>", self.saveAs)
        self.root.bind("<Control-e>", exit)
        self.root.bind("<Control-r>", self.run)

        self.text = Text(self.root, width=600, height=500)
        self.fontsize = 12
        self.text.config(borderwidth=0, tabs=spaces(4), background="black", foreground="white", insertbackground="white", font=("Consolas", self.fontsize))
        self.text.delete(0.0, END)
        self.text.bind("<KeyRelease>", self.check)
        self.text.tag_add("if", 0.0, END)
        self.text.tag_config("if", foreground="orange")
    def check(self, event):
        self.highlight("if", "black", "red", "")
        self.highlight("elif", "black", "red", "")
        self.highlight("else", "black", "red", "")
        self.highlight("import", "black", "red", "")
        self.highlight("from", "black", "red", "")
        self.highlight("as", "black", "red", "")
        self.highlight("return", "black", "red", "")
        self.highlight("#", "black", "#eeeeee", "")
        self.highlight("__init__", "black", "#1abc9c", "")
        self.highlight("'", "black", "yellow", "")
        self.highlight("\"", "black", "yellow", "")
        self.highlight("class", "black", "#3498db", ("Consolas", 12, "italic"))
        self.highlight("def", "black", "#3498db", ("Consolas", 12, "italic"))
        self.highlight("input", "black", "blue", ("Consolas", 12, "bold"))
        self.highlight("print", "black", "purple", "")
        self.highlight("global", "black", "purple", "")
    def fopen(self):
        global fn
        fn = fd.askopenfilename(title="Open", filetypes=(("Python Files", "*.py"), ("Python Files", "*.pyw")))
        f = open(fn, "r")
        fc = f.read()
        f.close()
        self.text.delete(0.0, END)
        self.text.insert(0.0, fc, END)
        pname = fn.split("/")
        pname = pname[len(pname)-1]
        self.root.title("Pedit - "+pname)
    def openf(self, event):
        self.fopen()
        self.check("")
    def makeMenu(self):
        self.menu = Menu(self.root)
        filemenu = Menu(self.menu)
        filemenu.add_command(label="Open (Ctrl+O)", command=lambda: self.openf(""))
        filemenu.add_command(label="Save (Ctrl+S)", command=lambda: self.save(""))
        filemenu.add_command(label="Save As (Ctrl+Shift+S)", command=lambda: self.saveAs(""))
        filemenu.add_separator()
        filemenu.add_command(label="Run (Ctrl+R)", command=lambda: self.run(""))
        filemenu.add_separator()
        filemenu.add_command(label="Exit (Ctrl+E)", command=exit)
        self.menu.add_cascade(label="File", menu=filemenu)
        self.editmenu = Menu(self.menu)
        self.editmenu.add_command(label="Toggle Line Numbers")
        self.menu.add_cascade(label="Edit", menu=self.editmenu)
        self.root.config(menu=self.menu)
    def launch(self):
        self.text.pack()
        self.root.mainloop()

app = MainApplication("Pedit")
app.makeMenu()
app.launch()
