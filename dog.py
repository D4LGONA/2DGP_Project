from pico2d import *
import game_framework
import game_world
from math import *
import random

import huddle_mode

G = 2

'''
 ** Todo list **
 Jump 가속도 수정하기

'''

state = {"stop_left": 0, "stop_right": 1, "stop_up" : 2, "stop_down": 3,
         "run_ld": 4, "run_ru": 5, "run_l": 6, "run_r": 7,
         "run_lu": 8, "run_rd": 9, "run_u": 10, "run_d": 11, "idle": 12}

# 강아지 속도 20km/h로 갈기고 여기서 36003600이니까 720미터 정도로 할까 가로 세로
PIXEL_PER_METER = (3600 / 72)  # 1미터 50픽셀?
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

def fail(e):
    return e[0] == 'FAIL'

def collision_with_AF(e):
    return e[0] == 'COLL_AF'

def collision_with_TN(e):
    return e[0] == 'COLL_TN'

def collision_with_WP(e):
    return e[0] == 'COLL_WP'

def Lshift_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LSHIFT

# 상태 목록: idle, run, stop, jump
class Idle:

    @staticmethod
    def enter(c, e):
        c.face_dir = 'idle'

    @staticmethod
    def exit(c, e):
        pass

    @staticmethod
    def do(c):
        c.shadowX = c.x
        c.shadowY = c.y
        c.frameX = (c.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2


        pass

    @staticmethod
    def draw(c):
        c.frameY = state[c.face_dir]
        sx, sy = c.x - c.bg.window_left, c.y - c.bg.window_bottom
        c.shadow.draw(c.shadowX - c.bg.window_left, c.shadowY - c.bg.window_bottom - 20, 64, 20)
        c.image.clip_draw(int(c.frameX) * 32, int(c.frameY) * 32, 32, 32, sx, sy, 64, 64)


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
        sx, sy = c.x - c.bg.window_left, c.y - c.bg.window_bottom
        c.shadow.draw(c.shadowX - c.bg.window_left, c.shadowY - c.bg.window_bottom - 20, 64, 20)
        c.image.clip_draw(int(c.frameX) * 32, int(c.frameY) * 32, 32, 32, sx, sy, 64, 64)


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
        c.shadowY = c.y - c.jump

        if get_time() - c.jumptime < 0.4:
            c.jump += G
            c.y += G
        elif get_time() - c.jumptime < 0.8:
            c.jump -= G
            c.y -= G
        else:
            c.state_machine.handle_event(('TIME_OUT', 0))


    @staticmethod
    def draw(c):
        c.frameY = state[c.face_dir]
        sx, sy = c.x - c.bg.window_left, c.y - c.bg.window_bottom
        c.shadow.draw(c.shadowX - c.bg.window_left, c.shadowY - c.bg.window_bottom - 20, 64, 20)
        c.image.clip_draw(int(c.frameX) * 32, int(c.frameY) * 32, 32, 32, sx, sy + c.jump, 64, 64)
        pass

class A_frame:
    @staticmethod
    def enter(c, e):
        c.Fail = False
        c.is_up = True
        c.frameY = state[c.face_dir]
        pass

    @staticmethod
    def exit(c, e):
        pass

    @staticmethod
    def do(c):
        if not c.Fail and random.randint(0, 100) == 1:
            if c.face_dir == 'run_ru':
                c.face_dir = 'run_rd'
            else:
                c.face_dir = 'run_ld'
            c.Fail = True
            c.shadowY -= 100

        if c.is_up and not c.Fail: # 올라가는중
            if c.face_dir == 'run_ru' and c.x > c.col_obj.x:
                c.face_dir = 'run_rd'
                c.is_up = False
                c.dirY *= -1
                game_world.move_depth(c.col_obj, 3)
            elif c.face_dir == 'run_lu' and c.x < c.col_obj.x:
                c.is_up = False
                c.face_dir = 'run_ld'
                c.dirY *= -1
                game_world.move_depth(c.col_obj, 3)
        elif not c.is_up and not c.Fail: # 내려가는중
            if c.col_obj.state == 'left':
                dest = c.col_obj.x + 40
            else:
                dest = c.col_obj.x - 40
            if (c.col_obj.state == 'left' and c.x > dest) or (c.col_obj.state == 'right' and c.x < dest):
                game_framework.get_mode()[-1].success_count += 1
                game_framework.get_mode()[-1].obstacle_count -= 1
                c.dirY = 0
                if c.face_dir == 'run_rd':
                    c.face_dir = 'run_r'
                    c.dirX = 1
                else:
                    c.face_dir = 'run_l'
                    c.dirX = -1
                c.state_machine.handle_event(('TIME_OUT', 0))
        else: # Fail
            game_world.move_depth(c.col_obj, 1)
            if c.y < c.col_obj.y - 100: # 이케 해도 되나
                game_framework.get_mode()[-1].fail_count += 1
                game_framework.get_mode()[-1].obstacle_count -= 1
                c.state_machine.handle_event(('FAIL', 0))
            else:
                c.dirY = -1
                c.dirX = 0
                c.face_dir = 'run_d'


        c.frameX = (c.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        c.x += c.dirX * RUN_SPEED_PPS * game_framework.frame_time
        c.y += c.dirY * RUN_SPEED_PPS * game_framework.frame_time
        c.shadowX = c.x
        c.shadowY = c.y

    @staticmethod
    def draw(c):
        c.frameY = state[c.face_dir]
        sx, sy = c.x - c.bg.window_left, c.y - c.bg.window_bottom
        c.shadow.draw(c.shadowX - c.bg.window_left, c.shadowY - c.bg.window_bottom - 20, 64, 20)
        c.image.clip_draw(int(c.frameX) * 32, int(c.frameY) * 32, 32, 32, sx, sy, 64, 64)
        pass

class Tunnel:

    @staticmethod
    def enter(c, e):
        c.Fail = False
        if c.col_obj.state == 'right_straight' or c.col_obj.state == 'left_straight':
            c.is_curve = False
        else:
            c.is_curve = True
        c.turn = False
        c.frameY = state[c.face_dir]
        pass

    @staticmethod
    def exit(c, e):
        pass

    @staticmethod
    def do(c):
        if c.is_curve:
            if c.col_obj.state == "left_curve":
                if c.turn and c.x < c.col_obj.x - 128:
                    game_framework.get_mode()[-1].success_count += 1
                    game_framework.get_mode()[-1].obstacle_count -= 1
                    c.state_machine.handle_event(('TIME_OUT', 0))
                if not c.turn and c.x > c.col_obj.x + 64:
                    c.dirX *= -1
                    c.turn = True
                    c.face_dir = 'run_l'
            else:
                if c.turn and c.x > c.col_obj.x + 128:
                    game_framework.get_mode()[-1].success_count += 1
                    game_framework.get_mode()[-1].obstacle_count -= 1
                    c.state_machine.handle_event(('TIME_OUT', 0))
                if not c.turn and c.x < c.col_obj.x - 64:
                    c.dirX *= -1
                    c.turn = True
                    c.face_dir = 'run_r'
        else:
            if c.col_obj.state == "left_straight":
                if c.x > c.col_obj.x + 128:
                    game_framework.get_mode()[-1].success_count += 1
                    game_framework.get_mode()[-1].obstacle_count -= 1
                    c.state_machine.handle_event(('TIME_OUT', 0))
            else:
                if c.x < c.col_obj.x - 128:
                    game_framework.get_mode()[-1].success_count += 1
                    game_framework.get_mode()[-1].obstacle_count -= 1
                    c.state_machine.handle_event(('TIME_OUT', 0))

        c.frameX = (c.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        c.x += c.dirX * RUN_SPEED_PPS * game_framework.frame_time
        c.y += c.dirY * RUN_SPEED_PPS * game_framework.frame_time

        c.shadowX = c.x
        c.shadowY = c.y

    @staticmethod
    def draw(c):
        c.frameY = state[c.face_dir]
        sx, sy = c.x - c.bg.window_left, c.y - c.bg.window_bottom
        c.shadow.draw(c.shadowX - c.bg.window_left, c.shadowY - c.bg.window_bottom - 20, 64, 20)
        c.image.clip_draw(int(c.frameX) * 32, int(c.frameY) * 32, 32, 32, sx, sy + c.jump, 64, 64)
        pass

class Weavepole:
    @staticmethod
    def enter(c, e):
        c.frameY = state[c.face_dir]
        c.start_time = get_time()
        c.col_obj.iscoll = True
        pass

    @staticmethod
    def exit(c, e):
        c.col_obj.iscoll = False
        pass

    @staticmethod
    def do(c):
        if get_time() - c.start_time > 0.5:
            c.dirX = 0
            c.state_machine.handle_event(('FAIL', 0))
            game_framework.get_mode()[-1].fail_count += 1
            game_framework.get_mode()[-1].obstacle_count -= 1

        if c.dirX > 0:
            if c.x > c.col_obj.x + 150:
                c.state_machine.handle_event(('TIME_OUT', 0))
                game_framework.get_mode()[-1].success_count += 1
                game_framework.get_mode()[-1].obstacle_count -= 1
        else:
            if c.x < c.col_obj.x - 150:
                c.state_machine.handle_event(('TIME_OUT', 0))
                game_framework.get_mode()[-1].success_count += 1
                game_framework.get_mode()[-1].obstacle_count -= 1

        c.frameX = (c.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        c.x += c.dirX * RUN_SPEED_PPS * game_framework.frame_time / 2
        c.y += c.dirY * RUN_SPEED_PPS * game_framework.frame_time / 2

        c.shadowX = c.x
        c.shadowY = c.y

    @staticmethod
    def draw(c):
        c.frameY = state[c.face_dir]
        sx, sy = c.x - c.bg.window_left, c.y - c.bg.window_bottom
        c.shadow.draw(c.shadowX - c.bg.window_left, c.shadowY - c.bg.window_bottom - 20, 64, 20)
        c.image.clip_draw(int(c.frameX) * 32, int(c.frameY) * 32, 32, 32, sx, sy + c.jump, 64, 64)
        pass

class Stop:

    @staticmethod
    def enter(c, e):
        c.frameX = 0
        c.dirX, c.dirY = 0, 0
        pass

    @staticmethod
    def exit(c, e):
        pass

    @staticmethod
    def do(c):
        c.frameX = (c.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        pass

    @staticmethod
    def draw(c):
        c.frameY = state[c.face_dir]
        sx, sy = c.x - c.bg.window_left, c.y - c.bg.window_bottom
        c.shadow.draw(c.shadowX - c.bg.window_left, c.shadowY - c.bg.window_bottom - 20, 64, 20)
        c.image.clip_draw(int(c.frameX) * 32, int(c.frameY) * 32, 32, 32, sx, sy, 64, 64)
        pass

class StateMachine:
    def __init__(self, dog):
        self.dog = dog
        self.cur_state = Idle
        self.transitions = {
            Idle: {Lclick: Run, space_down: Jump, collision_with_AF: A_frame, collision_with_TN: Tunnel, collision_with_WP: Weavepole},
            Run: {Lclick: Run, ctrl_down: Stop, space_down: Jump, collision_with_AF: A_frame, collision_with_TN: Tunnel, collision_with_WP: Weavepole},
            Stop: {ctrl_up: Idle},
            Jump: {time_out: Run},
            A_frame: {time_out: Run, fail: Idle},
            Tunnel: {time_out: Run, fail: Run},
            Weavepole: {time_out: Run, Lshift_down: Weavepole, fail: Idle}
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
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())


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
        dx = x + self.bg.window_left
        dy = y + self.bg.window_bottom
        self.dirX = (dx-self.x) / dist((dx, dy), (self.x, self.y))
        self.dirY = (dy-self.y) / dist((dx, dy), (self.x, self.y))

    def get_bb(self):
        return (self.x - self.bg.window_left - 28, self.y - self.bg.window_bottom - 28 + self.jump
                , self.x - self.bg.window_left + 28, self.y - self.bg.window_bottom + 28 + self.jump)

    def handle_obs_collision(self, group, other, where):
        if where == 'left' or where == 'right':
            self.dirX *= -1.0
            if self.face_dir == 'run_r':
                self.face_dir = 'run_l'
            elif self.face_dir == 'run_l':
                self.face_dir = 'run_r'
            elif self.face_dir == 'run_ru':
                self.face_dir = 'run_lu'
            elif self.face_dir == 'run_lu':
                self.face_dir = 'run_ru'
            elif self.face_dir == 'run_rd':
                self.face_dir = 'run_ld'
            elif self.face_dir == 'run_ld':
                self.face_dir = 'run_rd'

        elif where == 'top' or where == 'bottom':
            self.dirY *= -1.0
            if self.face_dir == 'run_ru':
                self.face_dir = 'run_rd'
            elif self.face_dir == 'run_lu':
                self.face_dir = 'run_ld'
            elif self.face_dir == 'run_rd':
                self.face_dir = 'run_ru'
            elif self.face_dir == 'run_ld':
                self.face_dir = 'run_lu'
            elif self.face_dir == 'run_u':
                self.face_dir = 'run_d'
            elif self.face_dir == 'run_d':
                self.face_dir = 'run_u'


    def handle_collision(self, group, other):
        if group == 'dog:huddle':
            if not other.ischecked:
                other.ischecked = True
                huddle_mode.obstacle_count -= 1
                if self.isjump:
                    huddle_mode.success_count += 1
                else:
                    huddle_mode.fail_count += 1
                    other.iscoll = True

        elif group == 'dog:a_frame':
            if not other.ischecked:
                other.ischecked = True
                self.col_obj = other
                if other.state == 'right':
                    self.face_dir = "run_lu"
                    self.dirX = -1.0 / 2
                    self.dirY = math.sqrt(3) / 2
                else:
                    self.face_dir = "run_ru"
                    self.dirX = 1.0 / 2
                    self.dirY = math.sqrt(3) / 2
                self.state_machine.handle_event(('COLL_AF', 0))

        elif group == 'dog:seesaw':
            pass
        elif group == 'dog:tunnel':
            if not other.ischecked:
                other.ischecked = True
                self.col_obj = other
                if other.state == 'right_curve' or other.state == 'right_straight':
                    self.face_dir = 'run_l'
                    self.dirX = -1.0
                    if other.state == 'right_curve':
                        self.dirY = 0.1
                    else:
                        self.dirY = 0
                else:
                    self.face_dir = 'run_r'
                    self.dirX = 1.0
                    if other.state == 'left_curve':
                        self.dirY = 0.1
                    else:
                        self.dirY = 0
                self.state_machine.handle_event(('COLL_TN', 0))

        elif group == 'dog:weavepoles':
            if not other.ischecked:
                other.ischecked = True
                other.iscoll = True
                self.col_obj = other
                self.y = other.y - 40.0
                if self.face_dir == 'run_r' or self.face_dir == 'run_ru' or self.face_dir == 'run_rd':
                    self.face_dir = 'run_r'
                    self.dirX = 1.0
                    self.dirY = 0
                elif self.face_dir == 'run_l' or self.face_dir == 'run_lu'or self.face_dir == 'run_ld':
                    self.face_dir = 'run_l'
                    self.dirX = -1.0
                    self.dirY = 0
                self.state_machine.handle_event(('COLL_WP', 0))
            pass
