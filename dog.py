from pico2d import *
import game_framework
import game_world
from math import *

import huddle_mode

G = 1

'''
 ** Todo list **
 Jump 상태일 때 맵 보기로 넘어가면 제자리로 돌아오지 않는 문제
 -> 상태를 확인하고 map mode에서 update를 돌릴지 말지 설정하는 방법이 없을까?
 Jump 가속도 수정하기

'''

state = {"stop_left": 0, "stop_right": 1, "stop_up" : 2, "stop_down": 3,
         "run_ld": 4, "run_ru": 5, "run_l": 6, "run_r": 7,
         "run_lu": 8, "run_rd": 9, "run_u": 10, "run_d": 11, "idle": 12}

# 강아지 속도 10km/h로 갈기고 여기서 36003600이니까 720미터 정도로 할까 가로 세로
PIXEL_PER_METER = (3600 / 72)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

GRAVITY = 9.8

#키 입력 가져오는 것
def Lclick(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN and e[1].button == SDL_BUTTON_LEFT
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def ctrl_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LCTRL

def ctrl_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LCTRL

def time_out(e):
    return e[0] == 'TIME_OUT'

# time_out = lambda e : e[0] == 'TIME_OUT'

# 상태 목록: idle, run, stop, jump
class Idle:

    @staticmethod
    def enter(c, e):
        print("idle enter")
        c.face_dir = 'idle'

    @staticmethod
    def exit(c, e):
        pass

    @staticmethod
    def do(c):
        # print("idle 실행 중")
        c.shadowX = c.x
        c.shadowY = c.y
        c.frameX = (c.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        pass

    @staticmethod
    def draw(c):
        c.frameY = state[c.face_dir]
        c.image.clip_draw(int(c.frameX) * 32, c.frameY * 32, 32, 32, c.drawX, c.drawY, 64, 64)


class Run:

    @staticmethod
    def enter(c, e):
        pass

    @staticmethod
    def exit(c, e):
        pass

    @staticmethod
    def do(c):

        c.frameX = (c.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        c.x += c.dirX * RUN_SPEED_PPS * game_framework.frame_time
        c.y += c.dirY * RUN_SPEED_PPS * game_framework.frame_time
        c.shadowX = c.x
        c.shadowY = c.y
        pass

    @staticmethod
    def draw(c):
        c.frameY = state[c.face_dir]
        #c.image.clip_draw(int(c.frameX) * 32, c.frameY * 32, 32, 32, c.drawX, c.drawY, 64, 64)

class Jump:

    @staticmethod
    def enter(c, e):
        c.frameX = 0
        c.jumptime = get_time()
        c.isjump = True
        c.jump = 0.0
        pass

    @staticmethod
    def exit(c, e):
        c.isjump = False
        c.jump = 1.0
        pass

    @staticmethod
    def do(c):
        c.frameX = (c.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        c.x += c.dirX * RUN_SPEED_PPS * game_framework.frame_time
        c.y += c.dirY * RUN_SPEED_PPS * game_framework.frame_time

        c.shadowX = c.x
        c.shadowY = c.y
        c.shadowY -= c.jump

        if get_time() - c.jumptime < 0.5:
            c.jump += G
            c.y += G
        elif get_time() - c.jumptime < 1.0:
            c.jump -= G
            c.y -= G
        else:
            c.state_machine.handle_event(('TIME_OUT', 0))


    @staticmethod
    def draw(c):
        c.frameY = state[c.face_dir]
        c.image.clip_draw(int(c.frameX) * 32, c.frameY * 32, 32, 32, c.drawX, c.drawY, 64, 64)
        pass


class Stop:

    @staticmethod
    def enter(c, e):
        c.frameX = 0
        pass

    @staticmethod
    def exit(c, e):
        pass

    @staticmethod
    def do(c):
        #c.frameX = (c.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        pass

    @staticmethod
    def draw(c):
        c.frameY = state[c.face_dir]
        c.image.clip_draw(int(c.frameX) * 32, c.frameY * 32, 32, 32, c.drawX, c.drawY, 64, 64)
        pass

class StateMachine:
    def __init__(self, dog):
        self.dog = dog
        self.cur_state = Idle
        self.transitions = {
            Idle: {Lclick: Run, space_down: Jump},
            Run: {Lclick: Run, ctrl_down: Stop, space_down: Jump},
            Stop: {ctrl_up: Idle},
            Jump: {time_out: Run}
        }

    def start(self):
        self.cur_state.enter(self.dog, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.dog)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.dog, e)
                self.cur_state = next_state
                self.cur_state.enter(self.dog, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.dog)


class Dog: # 강아지 캐릭터

    def __init__(self):
        self.x, self.y = 300, 300
        self.frameX, self.frameY = 0, 0
        self.image = load_image('resources/dog1.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.face_dir = 'idle'
        self.isjump = False
        self.dirX, self.dirY = 0, 0
        self.shadowX, self.shadowY = 300, 300
        self.shadow = load_image('resources/shadow.png')
        self.jump = 0.0

    def update(self):
        self.state_machine.update()

        self.x = clamp(32.0, self.x, self.bg.w - 32.0)
        self.y = clamp(32.0, self.y, self.bg.h - 32.0)

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):

        self.frameY = state[self.face_dir]
        sx, sy = self.x - self.bg.window_left, self.y - self.bg.window_bottom
        self.shadow.draw(self.shadowX - self.bg.window_left, self.shadowY - self.bg.window_bottom - 20, 64, 20)
        self.image.clip_draw(int(self.frameX) * 32, int(self.frameY) * 32, 32, 32, sx, sy, 64, 64)
        # self.state_machine.draw()
        # draw_rectangle(*self.get_bb())


    def set_background(self, bg):
        self.bg = bg
        self.x = self.bg.w / 2
        self.y = self.bg.h / 2

    def setface_dir(self, x, y):
        self.setDest(x, y)

        x1, y1 = self.x, self.y
        x2, y2 = self.x + 1, self.y
        slope1 = (y2-y1) / (x2-x1)
        slope2 = (y + self.bg.window_bottom - y1) / (x + self.bg.window_left - x1)

        angle_radians = math.atan2((slope2 - slope1) ,(1 + slope1 * slope2))
        angle_degrees = math.degrees(angle_radians)
        angle_degrees = (angle_degrees + 360) % 360
        if x + self.bg.window_left < self.x:
            angle_degrees = (angle_degrees + 180) % 360
        print(angle_degrees)

        if angle_degrees > 22.5 and angle_degrees <= 45 + 22.5:
            self.face_dir = "run_ru"
        elif angle_degrees > 45 + 22.5 and angle_degrees <= 90 + 22.5:
            self.face_dir = "run_u"
        elif angle_degrees > 90 + 22.5 and angle_degrees <= 135 + 22.5:
            self.face_dir = "run_lu"
        elif angle_degrees > 135 + 22.5 and angle_degrees <= 180 + 22.5:
            self.face_dir = "run_l"
        elif angle_degrees > 180 + 22.5 and angle_degrees <= 225 + 22.5:
            self.face_dir = "run_ld"
        elif angle_degrees > 225 + 22.5 and angle_degrees <= 270 + 22.5:
            self.face_dir = "run_d"
        elif angle_degrees > 270 + 22.5 and angle_degrees <= 315 + 22.5:
            self.face_dir = "run_rd"
        else:
            self.face_dir = "run_r"



    def setDest(self, x, y): # 목적지와 방향 정하는 것
        # x, y가 300, 300에서 얼마나 떨어져 있는지 확인 하기 x - 300, y - 300 얘를 정규화 x,y랑 300300
        print(self.x, self.y)
        dx = x + self.bg.window_left
        dy = y + self.bg.window_bottom
        self.dirX = (dx-self.x) / dist((dx, dy), (self.x, self.y))
        self.dirY = (dy-self.y) / dist((dx, dy), (self.x, self.y))

    def get_bb(self):
        return self.x - 32, self.y - 32, self.x + 32, self.y + 32

    def handle_collision(self, group, other):
        if group == 'dog:huddle':
            if not other.ischecked:
                other.ischecked = True
                huddle_mode.huddle_count -= 1
                if self.isjump:
                    huddle_mode.success_count += 1
                else:
                    huddle_mode.fail_count += 1
                    other.iscoll = True
