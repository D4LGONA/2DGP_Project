import pico2d
import game_framework
import game_world
import huddle_mode
from map import Map


def init():
    global map
    map = Map()
    map.centerPT(huddle_mode.centerX, huddle_mode.centerY)
    game_world.add_object(map, 3)
    pass

def finish():
    game_world.remove_object(map)
    pass

def update(): # Todo: 여기 어떻게 해결할 지 고민해야 함
    #game_world.update()
    map.centerPT(huddle_mode.centerX, huddle_mode.centerY)
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
        elif (event.type, event.key) == (pico2d.SDL_KEYDOWN, pico2d.SDLK_SPACE):
            game_framework.change_mode(huddle_mode)
        elif event.type == pico2d.SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_ESCAPE:
                    game_framework.pop_mode()
                case pico2d.SDLK_m:
                    game_framework.pop_mode()
    pass

