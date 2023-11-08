from pico2d import load_image
from math import *

class Background:
    def __init__(self, x = 200, y = 200):
        self.image = load_image('resources/bg.png')
        self.x, self.y = x, y
        self.destX, self.destY = x, y
        self.count = 0
        self.speed = 0
        self.dirX, self.dirY = 0.0, 0.0

    def draw(self):
        self.image.draw(self.x, self.y, 1600, 1600)

    def setDest(self, x, y):
        self.destX, self.destY = x, y
        self.dirX = (self.destX - self.x) / dist(self.destX, self.destY, self.x, self.y)
        self.dirY = (self.destY - self.y) / dist(self.destX, self.destY, self.x, self.y)

    def update(self):
        if self.destX is not self.x:
            self.destX += self.dirX * self.speed
            self.destY += self.dirY * self.speed
        pass
