# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import *

import game_world
from ball import Ball


# state event check
# ( state event type, event value )

def Lclick(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN and e[1].key == SDL_BUTTON_LEFT
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def ctrl_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LCTRL

def ctrl_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LCTRL

def time_out(e):
    return e[0] == 'TIME_OUT'

# time_out = lambda e : e[0] == 'TIME_OUT'


# todo: state에 있어야 할 것은 무엇이 있는가 -
#  달리는 모습(run:좌클릭 눌렀을 때), 서있는 모습(idle:run에서 목적지 닿았을때),
#  앉아있는 모습(idle, run에서 lctrl눌렀을때), 점프하는 모습 ??? space눌러씅ㄹ때

class Idle:

    @staticmethod
    def enter(c, e):
        if c.dir.x == -1:
            c.action = 2
        elif c.face_dir == 1:
            c.action = 3
        c.dir = 0
        c.frame = 0
        c.wait_time = get_time() # pico2d import 필요
        pass

    @staticmethod
    def exit(c, e):
        if space_down(e):
            c.fire_ball()
        pass

    @staticmethod
    def do(c):
        c.frame = (c.frame + 1) % 8
        if get_time() - c.wait_time > 2:
            c.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(c):
        c.image.clip_draw(c.frame * 100, c.action * 100, 100, 100, c.x, c.y)



class Run:

    @staticmethod
    def enter(c, e):
        pass

    @staticmethod
    def exit(c, e):
        pass

    @staticmethod
    def do(c):
        # todo : 프레임 넘기는 거랑 움직이는거 해야 함
        pass

    @staticmethod
    def draw(c):
        c.image.clip_draw(c.frameX * 32, c.frameY * 32, 32, 32, c.x, c.y) # 이미지 크기는 32*32

class Jump:

    @staticmethod
    def enter(c, e):
        c.frame = 0
        pass

    @staticmethod
    def exit(c, e):

        pass

    @staticmethod
    def do(c): # todo: frame 증가, 위치 이동
        c.frame = (c.frame + 1) % 8

    @staticmethod
    def draw(c):
        if c.face_dir == -1:
            pass
        else:
            pass
        pass


class Stop:

    @staticmethod
    def enter(c, e):
        c.frame = 0
        pass

    @staticmethod
    def exit(c, e):

        pass

    @staticmethod
    def do(c):
        c.frame = (c.frame + 1) % 8

    @staticmethod
    def draw(c):
        if c.face_dir == -1:
            pass
        else:
            pass
        pass


class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Idle
        self.transitions = {
            Idle: {Lclick: Run, space_down: Jump, ctrl_down: Stop},
            Run: {},
            Stop: {ctrl_up: Idle}
        }

    def start(self):
        self.cur_state.enter(self.boy, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.boy)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.boy)





class character:
    def __init__(self):
        self.x, self.y = 200, 200 # 화면 정 중앙에 그리기
        self.frameX, self.frameY = 0, 0
        self.image = load_image('resources/TestDog2.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

