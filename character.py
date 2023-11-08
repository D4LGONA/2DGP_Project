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

# 강아지 속도 10km/h로 갈기고 여기서 36003600이니까 720미터 정도로 할까 가로 세로
PIXEL_PER_METER = (3600 / 72)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

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
        print("idle 실행 중")
        pass

    @staticmethod
    def draw(c):
        c.image.clip_draw(c.frameX * 32, c.frameY * 32, 32, 32, c.drawX, c.drawY, 64, 64)



class Run:

    @staticmethod
    def enter(c, e):
        c.frameY = 2
        pass

    @staticmethod
    def exit(c, e):
        pass

    @staticmethod
    def do(c):
        # todo : 프레임 넘기는 거랑 움직이는거 해야 함
        print("run 실행 중")
        c.frameX = (c.frameX + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        pass

    @staticmethod
    def draw(c):
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
            c.frameY = 0
            c.drawY -= 1
        else:
            c.state_machine.handle_event(('TIME_OUT', 0))


    @staticmethod
    def draw(c):
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
            Run: {Lclick: Run, ctrl_down: Stop},
            Stop: {ctrl_up: Idle},
            Jump: {time_out: Idle}
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





class Character: # 강아지 캐릭터


    def __init__(self):
        self.drawX, self.drawY= 300, 300 # 화면 정 중앙에 그리기
        #self.x, self.y = 300, 300
        self.frameX, self.frameY = 0, 0
        self.image = load_image('resources/TestDog2.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.face_dir = 1


    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

