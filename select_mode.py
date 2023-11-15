from pico2d import *
import game_framework
import game_world
import huddle_mode
from map import Map

class Selectmode:
    def __init__(self, s):
        self.image = load_image(s)
        self.x, self.y = 300, 300

    def draw(self):
        self.image.draw(self.x, self.y, 600, 600)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def check_start(self, x, y):
        tmp = self.get_bb()
        if tmp[0] <= x <= tmp[2] and tmp[1] <= y <= tmp[3]:
            game_framework.change_mode(huddle_mode)

    def get_bb(self):
        return self.x - 150, self.y - 270, self.x + 120, self.y - 160
        pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                pass

    pass


def init():

    pass

def finish():
    pass

def update():
    game_world.update()
    pass

def draw():
    pico2d.clear_canvas()
    game_world.render()
    pico2d.update_canvas()
    pass



