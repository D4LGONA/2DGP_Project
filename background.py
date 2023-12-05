import pico2d
from pico2d import *
import game_framework

class Background:
    def __init__(self):
        self.bgm = pico2d.load_music('resources/스노우브라더스 BGM - World1.mp3')
        self.bgm.set_volume(30)
        self.bgm.repeat_play()

        self.image = load_image('resources/bg.png')
        self.cw = 600
        self.ch = 600
        self.w = self.image.w
        self.h = self.image.h



    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)

    def update(self):
        if game_framework.get_mode()[-1].dog.isjump:
            self.window_left = clamp(0, int(game_framework.get_mode()[-1].dog.x) - self.cw // 2, self.w - self.cw - 1)
            self.window_bottom = clamp(0, int(game_framework.get_mode()[-1].dog.y - game_framework.get_mode()[-1].dog.jump) - self.ch // 2, self.h - self.ch - 1)

        else:
            self.window_left = clamp(0, int(game_framework.get_mode()[-1].dog.x) - self.cw // 2, self.w - self.cw - 1)
            self.window_bottom = clamp(0, int(game_framework.get_mode()[-1].dog.y) - self.ch // 2 , self.h - self.ch - 1)
