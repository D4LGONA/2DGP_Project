import random
from pico2d import *
import game_framework
import game_world
from background import Background
from dog import Dog, Idle, Run
import map_mode
from tunnel import Tunnel
import clear_mode

success_count = 0
fail_count = 0
timer = 0.0
start_time = 0.0
timerStart = False
obstacle_count = 20

def handle_events():
    global timerStart, timer, start_time, success_count, fail_count, obstacle_count
    events = get_events()
    for event in events:
        dog.handle_event(event)
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_m:
                dog.state_machine.cur_state = Idle
                game_framework.push_mode(map_mode)
            elif event.key == SDLK_c:
                success_count = 20
                fail_count = 0
                obstacle_count = 0
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
    global t

    global font
    font = load_font('ENCR10B.TTF', 16)

    dog = Dog()
    bg = Background()
    t = [Tunnel(i + 1) for i in range(20)]

    game_world.add_object(bg, 0)
    game_world.add_object(dog, 2)
    game_world.add_objects(t, 1)

    game_world.add_collision_pair('dog:tunnel', dog, None)
    for i in t:
        game_world.add_collision_pair('dog:tunnel', None, i)

    for i in t:
        game_world.add_collision_pair('tunnel:tunnel', i, i)

    dog.set_background(bg)

    while True:
        flag = False
        if game_world.handle_init_collisions('tunnel:tunnel'): flag = True
        if flag: break


def finish():
    game_world.clear()
    pass


def update():
    global timer
    if not timerStart:
        timer = 0.0
    else:
        timer = get_time() - start_time
    game_world.update()
    game_world.handle_collisions('dog:tunnel')
    if dog.state_machine.cur_state == Run:
        game_world.handle_obs_collisions('dog:tunnel')

    if obstacle_count == 0:
        game_framework.push_mode(clear_mode)

def draw():
    clear_canvas()
    game_world.render()
    font.draw(600 - 200, 600 - 20, f'PLAYTIME: {timer:0.2f}', (0, 0, 0))
    font.draw(600 - 200, 600 - 40, f'SUCCESS: {success_count}', (0, 0, 0))
    font.draw(600 - 200, 600 - 60, f'FAIL: {fail_count}', (0, 0, 0))
    font.draw(600 - 200, 600 - 80, f'REMAIN: {obstacle_count} / 20', (0,0,0))
    update_canvas()

def pause():
    pass

def resume():
    pass

