from pico2d import *

class Map:
    def __init__(self):
        self.image = load_image('resources/bg.png')
        self.cx = 300
        self.cy = 300

    def centerPT(self, x, y):
        self.cx = x
        self.cy = y

    def draw(self):
        self.image.draw(300, 300, 600, 600)
        draw_rectangle((self.cx - 32)/6, (self.cy - 32)/6, (self.cx + 32)/6, (self.cy + 32)/6 )

    def update(self):
        pass