import random
from pico2d import *
import game_framework
import game_world
import map
import select_mode_2
from background import Background
from dog import Dog, Idle
import map_mode
from huddle import Huddle

centerX = 300
centerY = 300

success_count = 0
fail_count = 0
timer = 0.0
start_time = 0.0
timerStart = False
huddle_count = 20

def handle_events():
    global timerStart, timer, start_time
    events = get_events()
    for event in events:
        dog.handle_event(event)
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_mode(select_mode_2)
            elif event.key == SDLK_m:
                dog.state_machine.cur_state = Idle
                game_framework.push_mode(map_mode)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                if not timerStart:
                    timerStart = True
                    timer = 0.0
                    start_time = get_time()
                dog.setface_dir(event.x, 600 - 1 - event.y)
                dog.handle_event(event)

def init():
    global dog
    global bg
    global huddle

    global font
    font = load_font('ENCR10B.TTF', 16)

    dog = Dog()
    bg = Background()
    huddle = [Huddle(i + 1) for i in range(20)]

    game_world.add_object(bg, 0)
    game_world.add_object(dog, 2)
    game_world.add_objects(huddle, 1)

    game_world.add_collision_pair('dog:huddle', dog, None)
    for i in huddle:
        game_world.add_collision_pair('dog:huddle', None, i)

    for i in huddle:
        game_world.add_collision_pair('huddle:huddle', i, None)
        for j in huddle:
            if i is not j:
                game_world.add_collision_pair('huddle:huddle', None, j)

    dog.set_background(bg)

    pass

def finish(): # Todo: 객체가 지워지지 않아요 ㅠㅠ
    game_world.clear()
    pass


def update():
    if huddle_count == 0:
        pass


    global timer
    if not timerStart:
        timer = 0.0
    else:
        timer = get_time() - start_time
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    font.draw(600 - 200, 600 - 20, f'PLAYTIME: {timer:0.2f}', (0, 0, 0))
    font.draw(600 - 200, 600 - 40, f'SUCCESS: {success_count}', (0, 0, 0))
    font.draw(600 - 200, 600 - 60, f'FAIL: {fail_count}', (0, 0, 0))
    font.draw(600 - 200, 600 - 80, f'REMAIN: {huddle_count} / 20', (0,0,0))
    update_canvas()

def pause():
    pass

def resume():
    pass

