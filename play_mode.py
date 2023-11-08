import random

from pico2d import *
import game_framework
import game_world
from background import Background
from character import Character

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.key == SDL_BUTTON_LEFT:
            bg.setDest(event.x, 600 - 1 - event.y)
        else:
            dog.handle_event(event)

def init():
    global dog
    global bg

    dog = Character()
    bg = Background()

    game_world.add_object(bg, 0)
    game_world.add_object(dog, 1)


    pass

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    # fill here
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

