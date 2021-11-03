from tkinter import Tk, Menu
from tkinter.filedialog import askopenfilename
from App.UI import UI

class Window:
    def __init__(self, title, width, height):
        self.Width = width
        self.Height= height
        self.Title = title
        self.WindowTk = Tk()
        self.Layer = UI(self.WindowTk)
        self.ConfigWindow()
    
    def ConfigWindow(self):
        self.WindowTk.title(self.Title)
        self.WindowTk.geometry(self.WindowGeometryCenter())
        self.WindowTk.grid_columnconfigure(0, weight=1)
        self.WindowTk.grid_rowconfigure(0, weight=1)
        self.ConfigMenu(self.WindowTk)

    def ConfigMenu(self, window):
        menubar = Menu(window)
        submenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=submenu)
        submenu.add_command(label="Open", command=self.BrowseFile)
        submenu.add_command(label="Save Images", command=self.SaveFile)
        window.config(menu=menubar)

    def BrowseFile(self):
        filepath = askopenfilename(title="Open Image", filetypes=[("image file", (".jpg"))])
        if filepath:
            self.Layer.SetImage(filepath)

    def SaveFile(self):
        self.Layer.SaveImage()

    def Update(self):
        self.WindowTk.mainloop()
    
    def WindowGeometryCenter(self):
        ws = self.WindowTk.winfo_screenwidth()
        hs = self.WindowTk.winfo_screenheight()
        x = (ws / 2) - (self.Width / 2)
        y = (hs / 2) - (self.Height / 2)
        return f"+{int(x)}+{int(y)}"

    def GetWidth(self):
        return self.Width

    def GetHeight(self):
        return self.Height
