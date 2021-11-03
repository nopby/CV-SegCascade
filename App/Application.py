from .Window import Window

class Application:
    def __init__(self, title, width, height):
        self.Window = Window(title, width, height)
    def run(self):
        self.Window.Update()