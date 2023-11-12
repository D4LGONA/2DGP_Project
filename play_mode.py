import random

from pico2d import *
import game_framework
import game_world
import pannel
from background import Background
from dog import Dog
import map_mode
from huddle import Huddle


centerX = 300
centerY = 300

def handle_events():
    events = get_events()
    for event in events:
        dog.handle_event(event)
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_m:
                game_framework.push_mode(map_mode)
            elif event.key == SDLK_LCTRL:
                if not dog.isjump:
                    bg.setStop()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                bg.setDest(event.x, 600 - 1 - event.y)
                huddle.setDest(event.x, 600 - 1 - event.y)
                dog.setface_dir(event.x, 600 - 1 - event.y)
                dog.handle_event(event)

def init():
    global dog
    global bg
    global huddle

    dog = Dog()
    bg = Background()
    huddle = Huddle(400, 400)

    game_world.add_object(bg, 0)
    game_world.add_object(dog, 2)
    game_world.add_object(huddle, 1)

    game_world.add_collision_pair('dog:huddle', dog, huddle)
    #game_world.add_collision_pair()
    pass

def finish():
    game_world.clear()
    pass


def update():
    global centerX, centerY
    game_world.update()
    for i in game_world.objects[1]:
        i.set_depth(dog)
    for i in game_world.objects[3]:
        i.set_depth(dog)
    centerX = bg.CX
    centerY = bg.CY
    # print(centerX, centerY)
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

