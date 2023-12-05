from pico2d import *
from dog import *
import game_framework
from random import *

import game_world


state = {"right": 0, "left": 1}

class Aframe:
    image = None
    font = None
    def __init__(self, num, x = randint(300, 3300), y = randint(300, 3300), s = list(state.keys())[randint(0, 1)]):
        if Aframe.image == None:
            Aframe.image = load_image('resources/Aframe.png')
        if Aframe.font == None:
            Aframe.font = load_font('ENCR10B.TTF', 16)
        self.ismoved = False
        self.ischecked = False
        self.number = num
        self.frameX, self.frameY = 0, 0
        self.x, self.y = x, y
        self.state = s
        self.iscoll = False
        self.dx, self.dy = self.x, self.y
        self.selected = False

    def draw(self):
        self.frameY = state[self.state]
        Aframe.image.clip_draw(int(self.frameX) * 32, self.frameY * 32, 32, 32,
                               self.dx, self.dy, 128, 128)
        self.font.draw(self.dx, self.dy+30, f'{self.number}')

    def update(self):
        self.dx, self.dy = self.x - game_framework.get_mode()[-1].bg.window_left, self.y - game_framework.get_mode()[-1].bg.window_bottom

        # Todo: 여기 방향에 따라 depth 이동하는거 수정하기
        if not game_framework.get_mode()[-1].dog.state_machine.cur_state == A_frame:
            self.set_depth()

    def set_depth(self):
        if self in game_world.objects[1]:
            if self.y - 20 < game_framework.get_mode()[-1].dog.y:
                game_world.move_depth(self, 3)
                self.ismoved = True
        elif self in game_world.objects[3]:
            if self.y - 20 > game_framework.get_mode()[-1].dog.y:
                game_world.move_depth(self, 1)


    def get_bb(self):
        if self.state == 'right':
            return self.dx + 32, self.dy - 64, self.dx + 64, self.dy - 16
        else:
            return self.dx - 64, self.dy - 64, self.dx - 32, self.dy - 16

    def get_obs_bb(self):
        return [[self.dx - 32, self.dy - 64, self.dx + 32, self.dy - 44]]

    def get_init_bb(self):
        return self.dx - 80, self.dy - 80, self.dx + 80, self.dy + 80


    def handle_collision(self, group, other): # 여기 고쳐야 함
        if group == 'a_frame:a_frame':
            if self is not other:
                self.x, self.y = randint(300, 3300), randint(300, 3300)
                self.dx, self.dy = self.x, self.y

