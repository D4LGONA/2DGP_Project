from pico2d import *
import game_framework

class Map:
    def __init__(self):
        self.image = load_image('resources/bg.png')
        self.cx = 300
        self.cy = 300

    def draw(self):
        self.image.draw(300, 300, 600, 600)
        game_framework.get_mode()[-2].dog.image.clip_draw(0, 12 * 32, 32, 32,
            int(game_framework.get_mode()[-2].dog.x / 6), int(game_framework.get_mode()[-2].dog.y / 6),
            32/6.0, 32/6.0)

    def update(self):
        pass