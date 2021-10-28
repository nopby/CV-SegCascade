import tkinter
class Window:
    def __init__(self, title, width, height):
        self.Width = width
        self.Height= height
        self.Title = title
        self.WindowTk = tkinter.Tk()
        self.ConfigWindow()
    
    def ConfigWindow(self):
        self.WindowTk.title(self.Title)
        self.WindowTk.geometry(self.WindowGeometryCenter())
        self.WindowTk.grid_columnconfigure(0, weight=1)
        self.WindowTk.grid_rowconfigure(0, weight=1)
        

    def Update(self):
        self.WindowTk.mainloop()
    
    def WindowGeometryCenter(self):
        ws = self.WindowTk.winfo_screenwidth()
        hs = self.WindowTk.winfo_screenheight()
        x = (ws / 2) - (self.Width / 2)
        y = (hs / 2) - (self.Height / 2)
        return f"+{int(x)}+{int(y)}"

    
    def GetNativeWindow(self):
        return self.WindowTk