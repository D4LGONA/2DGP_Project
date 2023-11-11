import pico2d
import game_framework
import game_world
import play_mode
from pannel import Pannel


def init():
    global pannel
    pannel = Pannel()
    pannel.centerPT(play_mode.centerX, play_mode.centerY)
    game_world.add_object(pannel, 3)
    pass

def finish():
    game_world.remove_object(pannel)
    pass

def update(): # Todo: 여기 어떻게 해결할 지 고민해야 함
    #game_world.update()
    pannel.centerPT(play_mode.centerX, play_mode.centerY)
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
            game_framework.change_mode(play_mode)
        elif event.type == pico2d.SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_ESCAPE:
                    game_framework.pop_mode()
                case pico2d.SDLK_m:
                    game_framework.pop_mode()
    pass

