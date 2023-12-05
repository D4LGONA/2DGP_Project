from pico2d import *
from dog import *
import game_framework
from random import *

import game_world


state = {"right_straight": 0, "right_curve": 1, "left_straight": 2, "left_curve": 3}

class Tunnel:
    image = None
    font = None
    def __init__(self, num, x = randint(300, 3300), y = randint(300, 3300), s = None):
        if Tunnel.image == None:
            Tunnel.image = load_image('resources/Tunnel.png')
        if Tunnel.font == None:
            Tunnel.font = load_font('ENCR10B.TTF', 16)
        self.ismoved = False
        self.ischecked = False
        self.number = num
        self.frameX, self.frameY = 0, 0
        self.x, self.y = x, y
        if s == None:
            self.state_value = randint(0, 3)
            self.state = [i for i, v in state.items() if v == self.state_value][0]
        else : self.state = s
        self.iscoll = False
        self.dx, self.dy = self.x, self.y
        self.selected = False

    def draw(self):
        self.frameY = state[self.state]
        Tunnel.image.clip_draw(int(self.frameX) * 64, self.frameY * 32, 64, 32,
                               self.dx, self.dy, 256, 128)
        self.font.draw(self.dx, self.dy+70, f'{self.number}')

    def update(self):
        self.dx, self.dy = self.x - game_framework.get_mode()[-1].bg.window_left, self.y - game_framework.get_mode()[-1].bg.window_bottom

        # Todo: 여기 방향에 따라 depth 이동하는거 수정하기
        if not game_framework.get_mode()[-1].dog.state_machine.cur_state == Tunnel:
            self.set_depth()

    def set_depth(self):
        if self in game_world.objects[1]:
            if self.y - 50 < game_framework.get_mode()[-1].dog.y:
                game_world.move_depth(self, 3)
                self.ismoved = True
        elif self in game_world.objects[3]:
            if self.y - 50 > game_framework.get_mode()[-1].dog.y:
                game_world.move_depth(self, 1)

    def get_bb(self):
        if self.state == 'right_curve' or self.state == 'right_straight':
            return self.dx + 100, self.dy - 20, self.dx + 110, self.dy - 10
        else:
            return self.dx - 110, self.dy - 20, self.dx - 100, self.dy - 10

    def get_obs_bb(self):
        if self.state == 'right_curve' or self.state == 'left_curve':
            return [[self.dx - 100, self.dy - 64, self.dx + 100, self.dy + 16]]
        else:
            return [[self.dx - 100, self.dy - 64, self.dx + 100, self.dy - 54]]

    def get_init_bb(self):
        return self.dx - 180, self.dy - 80, self.dx + 180, self.dy + 80

    def handle_collision(self, group, other): # 여기 고쳐야 함
        if group == 'tunnel:tunnel':
            if self is not other:
                self.x, self.y = randint(300, 3300), randint(300, 3300)
                self.dx, self.dy = self.x, self.y
