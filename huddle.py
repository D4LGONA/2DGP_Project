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
        self.x, self.y = randint(600, 3000), randint(600, 3000)
        self.CX, self.CY = self.x, self.y
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
        self.font.draw(self.x, self.y+30, f'{self.number}')


    def setDest(self, x, y): # 목적지와 방향 정하는 것
        # x, y가 300, 300에서 얼마나 떨어져 있는지 확인 하기 x - 300, y - 300 얘를 정규화 x,y랑 300300
        self.dirX = -1 * (x-300) / dist((x, y), (300, 300))
        self.dirY = -1 * (y-300) / dist((x, y), (300, 300))

    def setStop(self):
        self.dirX, self.dirY = 0, 0

    def update(self):
        if self.ismoved:
            self.ismoved = False
            return
        self.set_depth()

        if self.iscoll and self.frameX < 3:
            self.frameX = (self.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        self.x += self.dirX * dog.RUN_SPEED_PPS * game_framework.frame_time
        self.y += self.dirY * dog.RUN_SPEED_PPS * game_framework.frame_time

        self.x = min(max(self.x, self.CX - 3000), self.CX)
        self.y = min(max(self.y, self.CY - 3000), self.CY)
        pass

    def set_depth(self):
        if self in game_world.objects[1]:
            if self.y - 10 < 300:
                game_world.move_depth(self, 3)
                self.ismoved = True
        elif self in game_world.objects[3]:
            if self.y - 10 > 300:
                game_world.move_depth(self, 1)


    def get_bb(self):
        if self.state == "right2" or self.state == "left2":
            return self.x - 32, self.y - 50, self.x + 32, self.y
        else:
            return self.x - 32, self.y - 50, self.x + 32, self.y - 10

    def handle_collision(self, group, other): # 여기 고쳐야 함
        if group == 'huddle:huddle':
            if self is not other:
                self.x, self.y = randint(600, 3000), randint(600, 3000)
        pass

