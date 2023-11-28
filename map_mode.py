import pico2d
import game_framework
import game_world
from map import Map
from dog import Idle


def init():
    global map
    map = Map()
    game_framework.get_mode()[-2].dog.state_machine.cur_state = Idle
    game_world.add_object(map, 3)
    pass

def finish():

    game_world.remove_object(map)
    pass

def update(): # Todo: 훔... 엉망이군
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

