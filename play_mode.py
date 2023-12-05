import random
from pico2d import *
import game_framework
import game_world
import select_mode
import select_mode_2
import server
from background import Background
import dog as d
import map_mode
from huddle import Huddle
from seesaw import Seesaw
from tunnel import Tunnel
from a_frame import Aframe
from weavepoles import Weavepoles
import clear_mode

success_count = 0
fail_count = 0
timer = 0.0
start_time = 0.0
timerStart = False
obstacle_count = 15
is_recode = False

def handle_events():
    global timerStart, timer, start_time, success_count, fail_count, obstacle_count
    events = get_events()
    for event in events:
        dog.handle_event(event)
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                if is_recode:
                    game_framework.change_mode(select_mode)
                else:
                    game_framework.change_mode(select_mode_2)

            elif event.key == SDLK_m:
                dog.state_machine.handle_event(('TIME_OUT', 0))
                game_framework.push_mode(map_mode)
            elif event.key == SDLK_c:
                success_count = 15
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
    global lss
    global font
    global success_count, fail_count, timer, start_time, timerStart, obstacle_count

    success_count = 0
    fail_count = 0
    timer = 0.0
    start_time = 0.0
    timerStart = False
    obstacle_count = 15

    font = load_font('ENCR10B.TTF', 16)

    dog = d.Dog()
    bg = Background()
    lss = [Huddle(1,2400, 2000, "right1"), Tunnel(2, 3100, 2400,"left_curve"), Weavepoles(3, 1900, 2600), Weavepoles(3,0, 0),
           Tunnel(4, 300, 3300, "right_curve"), Seesaw(5, 2000, 3100, "left"), Huddle(6, 3300, 3300, "left2"),
           Aframe(7, 1800, 2800, "right"), Huddle(8, 1200, 2000, "right2"),
           Aframe(9, 600, 1800, "right"), Tunnel(10, 1200, 1200, "right_straight"), Seesaw(11, 1900, 1000, "left"),
           Tunnel(12, 2400, 900, "right_straight"), Huddle(13, 3000, 600, "right1"),
           Weavepoles(14, 1800, 400), Weavepoles(14, 1800, 400), Huddle(15, 600, 600, "left1")]

    lss[3].parent = lss[2]
    lss[2].son = lss[3]

    lss[15].parent = lss[14]
    lss[14].son = lss[15]

    game_world.add_object(bg, 0)
    game_world.add_object(dog, 2)
    game_world.add_objects(lss, 1)

    game_world.add_collision_pair('dog:huddle', dog, None)
    game_world.add_collision_pair('dog:seesaw', dog, None)
    game_world.add_collision_pair('dog:tunnel', dog, None)
    game_world.add_collision_pair('dog:a_frame', dog, None)
    game_world.add_collision_pair('dog:weavepoles', dog, None)

    for i in lss:
        if type(i) == Huddle:
            game_world.add_collision_pair('dog:huddle', None, i)
        elif type(i) == Seesaw:
            game_world.add_collision_pair('dog:seesaw', None, i)
        elif type(i) == Tunnel:
            game_world.add_collision_pair('dog:tunnel', None, i)
        elif type(i) == Aframe:
            game_world.add_collision_pair('dog:a_frame', None, i)
        elif type(i) == Weavepoles:
            game_world.add_collision_pair('dog:weavepoles', None, i)

    dog.set_background(bg)

    pass

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
    game_world.handle_collisions()
    if dog.state_machine.cur_state != d.Jump and dog.state_machine.cur_state != d.Tunnel:
        game_world.handle_obs_collisions()

    if obstacle_count == 0:
        if is_recode:
            server.rank_list.append([timer, success_count, fail_count])
            server.set_rank()
        game_framework.push_mode(clear_mode)

def draw():
    clear_canvas()
    game_world.render()
    font.draw(600 - 200, 600 - 20, f'PLAYTIME: {timer:0.2f}', (0, 0, 0))
    font.draw(600 - 200, 600 - 40, f'SUCCESS: {success_count}', (0, 0, 0))
    font.draw(600 - 200, 600 - 60, f'FAIL: {fail_count}', (0, 0, 0))
    font.draw(600 - 200, 600 - 80, f'REMAIN: {obstacle_count} / 15', (0,0,0))
    update_canvas()

def pause():
    pass

def resume():
    pass

