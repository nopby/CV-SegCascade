from .Window import Window
from .UI import UI

class Application:
    def __init__(self, title, width, height):
        self.Window = Window(title, width, height)
        self.Layer = UI(self.Window.GetNativeWindow())
    def run(self):
        self.Window.Update()