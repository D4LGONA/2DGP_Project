from pico2d import *
from math import *
import huddle_mode as play_mode
import server
import game_framework

class Background:
    def __init__(self):
        self.image = load_image('resources/bg.png')
        self.cw = 600
        self.ch = 600
        self.w = self.image.w
        self.h = self.image.h

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)

    def update(self):
        if game_framework.get_mode().dog.isjump:
            self.window_left = clamp(0, int(game_framework.get_mode().dog.x) - self.cw // 2, self.w - self.cw - 1)
            self.window_bottom = clamp(0, int(game_framework.get_mode().dog.y - game_framework.get_mode().dog.jump) - self.ch // 2, self.h - self.ch - 1)

        else:
            self.window_left = clamp(0, int(game_framework.get_mode().dog.x) - self.cw // 2, self.w - self.cw - 1)
            self.window_bottom = clamp(0, int(game_framework.get_mode().dog.y) - self.ch // 2 , self.h - self.ch - 1)
