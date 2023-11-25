from pico2d import *
import game_framework
import game_world
import huddle_mode
from map import Map

class Selectmode:
    def __init__(self):
        #self.image = load_image(s)
        self.x, self.y = 300, 300

    def draw(self):
        #self.image.draw(self.x, self.y, 600, 600)
        draw_rectangle(*self.get_practice())
        draw_rectangle(*self.get_start())
        draw_rectangle(*self.get_back())

    def update(self):
        pass

    def check_start(self, x, y):
        pass

    def get_start(self):
        return 200, 200, 400, 250

    def get_practice(self):
        return 200, 350, 400, 400

    def get_back(self):
        return 0, 600, 100, 550

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
    global sel

    sel = Selectmode()
    game_world.add_object(sel, 0)
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



