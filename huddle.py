from pico2d import *
from math import *
import dog
import game_framework
from random import *
import huddle_mode

import game_world

'''
** todo list **
순서대로 안넘으면 fail count 올리기
허들 넘는거 성공한 카운트 어떻게 잴지 다시 생각 해보기
'''

state = {"right2": 0, "left2": 1, "right1": 2, "left1": 3}

TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Huddle:
    image = None
    font = None
    def __init__(self, num):
        if Huddle.image == None:
            Huddle.image = load_image('resources/huddle.png')
        if Huddle.font == None:
            Huddle.font = load_font('ENCR10B.TTF', 16)
        self.ismoved = False
        self.ischecked = False
        self.number = num
        self.frameX, self.frameY = 0, 3
        self.x, self.y = randint(300, 3300), randint(300, 3300)
        self.state_value = randint(0, 3)
        self.state = [i for i, v in state.items() if v == self.state_value][0]
        self.iscoll = False
        self.dx, self.dy = self.x, self.y

    def draw(self):
        self.frameY = state[self.state]
        Huddle.image.clip_draw(int(self.frameX) * 64, self.frameY * 64, 64, 64,
                               self.dx, self.dy, 128, 128)
        draw_rectangle(*self.get_bb())

        draw_rectangle(*self.get_obs_bb()[0])
        draw_rectangle(*self.get_obs_bb()[1])
        self.font.draw(self.dx, self.dy+30, f'{self.number}')


    def update(self):

        if self.iscoll and self.frameX < 3:
            self.frameX = (self.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        self.dx, self.dy = self.x - game_framework.get_mode()[-1].bg.window_left, self.y - game_framework.get_mode()[-1].bg.window_bottom

        # Todo: 여기 방향에 따라 depth 이동하는거 수정하기
        if not game_framework.get_mode()[-1].dog.isjump:
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
        if self.state == "right2" or self.state == "left2":
            return self.dx - 32, self.dy - 50, self.dx + 32, self.dy
        else:
            return self.dx - 32, self.dy - 50, self.dx + 32, self.dy - 10

    def get_init_bb(self):
        return self.dx - 80, self.dy - 80, self.dx + 80, self.dy + 80

    def get_obs_bb(self):
        return [[self.dx - 60, self.dy - 50, self.dx - 40, self.dy - 40], [self.dx + 40, self.dy - 50, self.dx + 60, self.dy - 40]]

    def handle_collision(self, group, other):
        if group == 'huddle:huddle':
            if self is not other:
                self.x, self.y = randint(300, 3300), randint(300, 3300)
                self.dx, self.dy = self.x, self.y
        pass

