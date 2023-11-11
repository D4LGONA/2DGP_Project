import random

from pico2d import *
import game_framework
import game_world
import pannel
from background import Background
from dog import Dog
import map_mode


centerX = 300
centerY = 300

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            bg.setDest(event.x, 600 - 1 - event.y)
            dog.setface_dir(event.x, 600 - 1 - event.y)
            dog.handle_event(event)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_m:
            game_framework.push_mode(map_mode)
        else:
            dog.handle_event(event)

def init():
    global dog
    global bg

    dog = Dog()
    bg = Background()

    game_world.add_object(bg, 0)
    game_world.add_object(dog, 1)
    pass

def finish():
    game_world.clear()
    pass


def update():
    global centerX, centerY
    game_world.update()
    centerX = bg.CX
    centerY = bg.CY
    # print(centerX, centerY)
    # fill here
    #game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

