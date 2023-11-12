from pico2d import *
import game_framework
import game_world
from math import *

import huddle_mode

'''
 ** Todo list **
 Jump 상태일 때 맵 보기로 넘어가면 제자리로 돌아오지 않는 문제
 -> 상태를 확인하고 map mode에서 update를 돌릴지 말지 설정하는 방법이 없을까?
 Jump 가속도 수정하기
 강아지 리소스 수정하기(멈추는 것과 점프 모션을 다시 정할 것)
 

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


# todo: state에 있어야 할 것은 무엇이 있는가 -
#  달리는 모습(run:좌클릭 눌렀을 때), 서있는 모습(idle:run에서 목적지 닿았을때),
#  앉아있는 모습(idle, run에서 lctrl눌렀을때), 점프하는 모습 ??? space눌러씅ㄹ때

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
        c.x = min(max(c.x, 300), 3300)
        c.y = min(max(c.y, 300), 3300)
        pass

    @staticmethod
    def draw(c):
        c.frameY = state[c.face_dir]
        c.image.clip_draw(int(c.frameX) * 32, c.frameY * 32, 32, 32, c.drawX, c.drawY, 64, 64)

class Jump:

    @staticmethod
    def enter(c, e):
        c.frameX = 0
        c.jumptime = get_time()
        c.isjump = True
        pass

    @staticmethod
    def exit(c, e):
        c.isjump = False
        pass

    @staticmethod
    def do(c): # todo: frame 증가, 위치 이동
        c.frameX = (c.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        if get_time() - c.jumptime < 0.3:
            c.drawY += 1
        elif get_time() - c.jumptime < 0.6:
            # if c.face_dir == ""
            c.drawY -= 1
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
        self.drawX, self.drawY = 300, 300 # 화면 정 중앙에 그리기
        self.x, self.y = 300, 300
        self.frameX, self.frameY = 0, 0
        self.image = load_image('resources/dog1.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.face_dir = 'idle'
        self.isjump = False
        self.dirX, self.dirY = 0, 0

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def setface_dir(self, x, y):
        self.setDest(x, y)

        x1, y1 = 300, 300
        x2, y2 = 301, 300
        slope1 = (y2-y1) / (x2-x1)
        slope2 = (y-y1) / (x-x1)

        angle_radians = math.atan2((slope2 - slope1) ,(1 + slope1 * slope2))
        angle_degrees = math.degrees(angle_radians)
        angle_degrees = (angle_degrees + 360) % 360
        if x < 300:
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
        self.dirX = (x-300) / dist((x,y), (300, 300))
        self.dirY = (y-300) / dist((x, y), (300, 300))

    def get_bb(self):
        return self.drawX - 32, self.drawY - 32, self.drawX + 32, self.drawY + 32

    def handle_collision(self, group, other):
        if not self.isjump:
            other.iscoll = True
            if not other.ischecked:
                other.ischecked = True
                huddle_mode.fail_count += 1
