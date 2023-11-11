from pico2d import load_image
from math import *
import dog
import game_framework

bgWidth = 3600
bgHeight = 3600

class Background:
    def __init__(self, x = bgWidth // 2, y = bgHeight // 2):
        self.image = load_image('resources/bg.png')
        self.x, self.y = x, y
        self.count = 0
        self.speed = 1
        self.dirX, self.dirY = 0.0, 0.0
        self.CX, self.CY = 300, 300

    def draw(self):
        self.image.draw(self.x, self.y, bgWidth, bgHeight)

    def setDest(self, x, y): # 목적지와 방향 정하는 것
        # x, y가 300, 300에서 얼마나 떨어져 있는지 확인 하기 x - 300, y - 300 얘를 정규화 x,y랑 300300
        self.dirX = -1 * (x-300) / dist((x,y), (300, 300))
        self.dirY = -1 * (y-300) / dist((x, y), (300, 300))

    def setStop(self):
        self.dirX, self.dirY = 0, 0

    def update(self):
        self.x += self.dirX * dog.RUN_SPEED_PPS * game_framework.frame_time
        self.CX -= self.dirX * dog.RUN_SPEED_PPS * game_framework.frame_time
        self.y += self.dirY * dog.RUN_SPEED_PPS * game_framework.frame_time
        self.CY -= self.dirY * dog.RUN_SPEED_PPS * game_framework.frame_time
        self.x = min(max(self.x, -(bgWidth//2) + 600), bgWidth//2)
        self.CX = min(max(self.CX, 300), 3300)
        self.y = min(max(self.y, -(bgHeight//2) + 600), bgHeight//2)
        self.CY = min(max(self.CY, 300), 3300)
        pass
