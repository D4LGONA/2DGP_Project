from pico2d import *
from math import *
import dog
import game_framework
from random import *
import huddle_mode

import game_world


state = {"left": 0, "right": 1}

TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Seesaw:
    image = None
    font = None
    def __init__(self, num, x = randint(300, 3300), y = randint(300, 3300), s = list(state.keys())[randint(0, 1)]):
        if Seesaw.image == None:
            Seesaw.image = load_image('resources/seesaw.png')
        if Seesaw.font == None:
            Seesaw.font = load_font('ENCR10B.TTF', 16)
        self.ismoved = False
        self.ischecked = False
        self.number = num
        self.frameX, self.frameY = 0, 3
        self.x, self.y = x, y
        self.state = s
        self.iscoll = False
        self.dx, self.dy = self.x, self.y
        self.start_time = 0

    def draw(self):
        self.frameY = state[self.state]
        Seesaw.image.clip_draw(int(self.frameX) * 32, self.frameY * 32, 32, 32,
                               self.dx, self.dy, 128, 128)
        self.font.draw(self.dx, self.dy+60, f'{self.number}')

    def update(self): # fail 고쳐야

        self.dx, self.dy = self.x - game_framework.get_mode()[-1].bg.window_left, self.y - game_framework.get_mode()[-1].bg.window_bottom

        # Todo: 여기 방향에 따라 depth 이동하는거 수정하기
        if not game_framework.get_mode()[-1].dog.isjump and not self.iscoll:
            self.set_depth()

        if self.iscoll:
            if self.frameX == 0: game_world.move_depth(self, 1)
            elif self.frameX == 2: game_world.move_depth(self, 3)

        pass

    def set_depth(self):
        if self in game_world.objects[1]:
            if self.y - 20 < game_framework.get_mode()[-1].dog.y:
                game_world.move_depth(self, 3)
                self.ismoved = True
        elif self in game_world.objects[3]:
            if self.y - 20 > game_framework.get_mode()[-1].dog.y:
                game_world.move_depth(self, 1)


    def get_bb(self):
        if self.state == "right":
            return self.dx + 20, self.dy - 50, self.dx + 64, self.dy - 20
        else:
            return self.dx - 64, self.dy - 50, self.dx - 20, self.dy - 20

    def get_init_bb(self):
        return self.dx - 80, self.dy - 80, self.dx + 80, self.dy + 80

    def get_obs_bb(self):
        return [[self.dx - 5, self.dy - 50, self.dx + 5, self.dy - 40]]

    def handle_collision(self, group, other):
        if group == 'seesaw:seesaw':
            if self is not other:
                self.x, self.y = randint(300, 3300), randint(300, 3300)
                self.dx, self.dy = self.x, self.y
