# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import *
import game_framework
import game_world
from ball import Ball

# Todo: 속도 정해 줘야 함
# Todo: 클래스 이름 바꾸기
# 코드 이해할 수 있게 바꾸기
# 프레임 시간부터 하기
# Todo: 강아지가 이동하게 하려면 어떻게 해야 하는 거지?
# 함수 하나가 한 페이지를 넘어가지 않도록 해라 **

state = {"stop_left": 0, "stop_right": 1, "stop_up" : 2, "stop_down": 3,
         "run_ld": 4, "run_ru": 5, "run_l": 6, "run_r": 7,
         "run_lu": 8, "run_rd": 9, "run_u": 10, "run_d": 11, "idle": 12}

# 강아지 속도 10km/h로 갈기고 여기서 36003600이니까 720미터 정도로 할까 가로 세로
PIXEL_PER_METER = (3600 / 72)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
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
        c.frameX, c.frameY = 0, 3
        pass

    @staticmethod
    def exit(c, e):
        pass

    @staticmethod
    def do(c):
        # print("idle 실행 중")
        pass

    @staticmethod
    def draw(c):
        c.image.clip_draw(c.frameX * 32, c.frameY * 32, 32, 32, c.drawX, c.drawY, 64, 64)


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
        # print("run 실행 중")
        c.frameX = (c.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        pass

    @staticmethod
    def draw(c):
        c.frameY = state[c.face_dir]
        c.image.clip_draw(int(c.frameX) * 32, c.frameY * 32, 32, 32, c.drawX, c.drawY, 64, 64)

class Jump:

    @staticmethod
    def enter(c, e):
        c.frameX = 0
        c.frameY = 1
        c.jumptime = get_time()
        pass

    @staticmethod
    def exit(c, e):

        pass

    @staticmethod
    def do(c): # todo: frame 증가, 위치 이동
        c.frameX = (c.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        if get_time() - c.jumptime < 1:
            c.drawY += 1
        elif get_time() - c.jumptime < 2:
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
        c.frame = 0
        pass

    @staticmethod
    def exit(c, e):
        pass

    @staticmethod
    def do(c):
        c.frameX = (c.frameX + 1) % 2

    @staticmethod
    def draw(c):
        pass

class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Idle
        self.transitions = {
            Idle: {Lclick: Run, space_down: Jump, ctrl_down: Stop},
            Run: {Lclick: Run, ctrl_down: Stop, space_down: Jump},
            Stop: {ctrl_up: Idle},
            Jump: {time_out: Run}
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


class Dog: # 강아지 캐릭터

    def __init__(self):
        self.drawX, self.drawY = 300, 300 # 화면 정 중앙에 그리기
        self.frameX, self.frameY = 0, 0
        self.image = load_image('resources/dog1.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.face_dir = 'run_up'

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    def setface_dir(self, x, y):
        x1, y1 = 300, 300
        x2, y2 = 301, 300
        slope1 = (y2-y1) / (x2-x1)
        slope2 = (y-y1) / (x-x1)

        angle_radians = math.atan2((slope2 - slope1) ,(1 + slope1 * slope2))
        angle_degrees = math.degrees(angle_radians)
        # angle_radians = math.acos()
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