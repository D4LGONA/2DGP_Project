import random
from pico2d import *
import game_framework
import game_world
import pannel
from background import Background
from dog import Dog, Idle
import map_mode
from huddle import Huddle

centerX = 300
centerY = 300

success_count = 0
fail_count = 0
timer = 0.0
font = load_font('ENCR10B.TTF', 16)

def handle_events():
    global timer
    events = get_events()
    for event in events:
        dog.handle_event(event)
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_m:
                dog.drawX, dog.drawY = 300, 300
                dog.state_machine.cur_state = Idle
                game_framework.push_mode(map_mode)
            elif event.key == SDLK_LCTRL:
                if not dog.isjump:
                    bg.setStop()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                timer = get_time()
                bg.setDest(event.x, 600 - 1 - event.y)
                for i in huddle:
                    i.setDest(event.x, 600 - 1 - event.y)
                dog.setface_dir(event.x, 600 - 1 - event.y)
                dog.handle_event(event)

def init():
    global dog
    global bg
    global huddle

    dog = Dog()
    bg = Background()
    huddle = [Huddle() for _ in range(1)]

    game_world.add_object(bg, 0)
    game_world.add_object(dog, 2)
    game_world.add_objects(huddle, 1)

    game_world.add_collision_pair('dog:huddle', dog, None)
    for i in huddle:
        game_world.add_collision_pair('dog:huddle', None, i)
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
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    font.draw(600 - 10, 600 - 50, f'{timer:0.2f}', (255, 255, 0))
    update_canvas()

def pause():
    pass

def resume():
    pass

