from pico2d import *
from math import *
import dog
import game_framework
from random import *
import huddle_mode

import game_world

TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Weavepoles:
    image = None
    font = None
    def __init__(self, num,x = randint(300, 3300), y = randint(300, 3300),parent = None):
        if Weavepoles.image == None:
            Weavepoles.image = load_image('resources/weavepoles.png')
        if Weavepoles.font == None:
            Weavepoles.font = load_font('ENCR10B.TTF', 16)
        self.ismoved = False
        self.ischecked = False
        self.number = num
        self.frameX, self.frameY = 0, 3
        self.x, self.y = x, y
        self.iscoll = False
        self.dx, self.dy = self.x, self.y
        self.parent = parent
        self.son = None

    def draw(self):
        Weavepoles.image.clip_draw(int(self.frameX) * 64, 0, 64, 64,
                               self.dx, self.dy, 256, 128)
        if self.parent == None:
            Weavepoles.font.draw(self.dx, self.dy+100, f'{self.number}')


    def update(self):
        if self.son is not None and self.son.ischecked : self.ischecked = True
        if self.parent is not None and self.parent.ischecked : self.ischecked = True

        if self.parent is not None:
            self.x, self.y = self.parent.x + 24, self.parent.y + 8
            if self.parent.iscoll or self.iscoll:
                game_world.move_depth(self, 1)

        if self.son is not None:
            if self.son.iscoll or self.iscoll:
                game_world.move_depth(self, 3)

        self.dx, self.dy = self.x - game_framework.get_mode()[-1].bg.window_left, self.y - \
                               game_framework.get_mode()[-1].bg.window_bottom

        if not game_framework.get_mode()[-1].dog.state_machine.cur_state == dog.Weavepole:
            self.set_depth()

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
        if self.parent == None:
            return self.dx - 128 , self.dy - 50, self.dx - 110, self.dy - 40
        else:
            return self.dx + 110, self.dy - 50, self.dx + 128, self.dy - 40

    def get_init_bb(self):
        return self.dx - 150, self.dy - 100, self.dx + 150, self.dy + 100

    def get_obs_bb(self):
        return None

    def handle_collision(self, group, other):
        if group == 'weavepoles:weavepoles':
            if self is not other:
                self.x, self.y = randint(300, 3300), randint(300, 3300)
                self.dx, self.dy = self.x, self.y
        pass

