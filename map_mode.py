from pico2d import *
import game_framework
import game_world
from dog import Idle

class Map:
    def __init__(self):
        self.image = load_image('resources/bg.png')
        self.cx = 300
        self.cy = 300

    def draw(self):
        self.image.draw(300, 300, 600, 600)
        game_framework.get_mode()[-2].dog.image.clip_draw(0, 12 * 32, 32, 32,
            int(game_framework.get_mode()[-2].dog.x / 6), int(game_framework.get_mode()[-2].dog.y / 6),
            32/6.0, 32/6.0)

    def update(self):
        pass

def init():
    global map
    map = Map()
    game_framework.get_mode()[-2].dog.state_machine.cur_state = Idle
    game_world.add_object(map, 4)
    pass

def finish():
    game_world.remove_object(map)
    pass

def update():
    pass

def draw():
    pico2d.clear_canvas()
    game_world.render()
    pico2d.update_canvas()
    pass

def handle_events():
    events = pico2d.get_events()
    for event in events:
        if event.type == pico2d.SDL_QUIT:
            game_framework.quit()
        elif event.type == pico2d.SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_ESCAPE:
                    game_framework.pop_mode()
                case pico2d.SDLK_m:
                    game_framework.pop_mode()
    pass

