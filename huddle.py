from pico2d import load_image, draw_rectangle
from math import *
import dog
import game_framework
from random import *
import play_mode

import game_world

'''
** todo list **
update 부분 수정할 것(허들 이동 하는 것)
충돌처리
'''

state = {"right2": 0, "left2": 1, "right1": 2, "left1": 3}

TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Huddle:
    image = None
    def __init__(self, x = randint(600, 3000), y = randint(600, 3000)):
        if Huddle.image == None:
            Huddle.image = load_image('resources/huddle.png')
        self.frameX, self.frameY = 0, 3
        self.x, self.y = x, y
        self.CX, self.CY = x, y
        self.dirX, self.dirY = 0.0, 0.0
        self.state_value = randint(0, 3)
        self.state = [i for i, v in state.items() if v == self.state_value][0]
        self.iscoll = False
        print(self.state)
        print(self.x, self.y)

    def draw(self):
        self.frameY = state[self.state]
        Huddle.image.clip_draw(int(self.frameX) * 64, self.frameY * 64, 64, 64, self.x, self.y, 128, 128)
        draw_rectangle(*self.get_bb())

    def setDest(self, x, y): # 목적지와 방향 정하는 것
        # x, y가 300, 300에서 얼마나 떨어져 있는지 확인 하기 x - 300, y - 300 얘를 정규화 x,y랑 300300
        self.dirX = -1 * (x-300) / dist((x,y), (300, 300))
        self.dirY = -1 * (y-300) / dist((x, y), (300, 300))

    def setStop(self):
        self.dirX, self.dirY = 0, 0

    def update(self):
        if self.iscoll and self.frameX < 3:
            self.frameX = (self.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        self.x += self.dirX * dog.RUN_SPEED_PPS * game_framework.frame_time
        self.y += self.dirY * dog.RUN_SPEED_PPS * game_framework.frame_time

        self.x = min(max(self.x, self.CX - 3000), self.CX)
        self.y = min(max(self.y, self.CY - 3000), self.CY)
        pass

    def set_depth(self, dog):
        if self.y + 10 > dog.y:
            game_world.move_depth(self, 1)
        elif self.y + 10 < dog.y:
            game_world.move_depth(self, 3)

    def get_bb(self):
        if self.state == 0 or self.state == 1:
            return self.x - 32, self.y - 50, self.x + 32, self.y + 10
        else:
            return self.x - 32, self.y - 50, self.x + 32, self.y - 10

    def handle_collision(self, group, other):
        if group == 'dog:huddle':
            if not other.isjump:
                self.iscoll = True
