from pico2d import *
import game_framework
import game_world
import select_mode
import server
import title_mode
from dog import Idle

class Clear:
    def __init__(self):
        self.image = load_image('resources/clear.png')
        self.cx = 300
        self.cy = 300
        self.font = load_font('ENCR10B.TTF', 16)

    def draw(self):
        self.image.draw(300, 300, 400, 400)
        self.font.draw(300, 350, f'{game_framework.get_mode()[-2].success_count}', (0,0,0))
        self.font.draw(300, 310, f'{game_framework.get_mode()[-2].fail_count}', (0,0,0))
        self.font.draw(300, 270, f'{game_framework.get_mode()[-2].timer:0.2f}', (0,0,0))

    def update(self):
        pass

def init():
    global cl
    cl = Clear()
    game_world.add_object(cl, 4)
    server.rank_list.append([game_framework.get_mode()[-2].timer, game_framework.get_mode()[-2].success_count, game_framework.get_mode()[-2].fail_count])
    pass

def finish():
    game_world.remove_object(cl)
    pass

def update():
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
                    game_framework.change_mode(select_mode)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            match event.button:
                case SDL_BUTTON_LEFT:
                    game_framework.pop_mode()
                    game_framework.change_mode(select_mode)
    pass

