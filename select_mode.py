from pico2d import *
import game_framework
import game_world
import title_mode
import select_mode_2

class Selectmode:
    def __init__(self):
        self.image = load_image("resources/select_1.png")
        self.x, self.y = 300, 300

    def draw(self):
        self.image.draw(self.x, self.y, 600, 600)
        draw_rectangle(*self.get_practice())
        draw_rectangle(*self.get_start())
        draw_rectangle(*self.get_back())
        draw_rectangle(*self.get_ranking())

    def update(self):
        pass

    def check_click(self, x, y):
        if self.get_start()[0] < x < self.get_start()[2] and self.get_start()[1] < y < self.get_start()[3]:
            game_framework.change_mode(play_mode)
        elif self.get_practice()[0] < x < self.get_practice()[2] and self.get_practice()[1] < y < self.get_practice()[3]:
            game_framework.change_mode(select_mode_2)
        elif self.get_ranking()[0] < x < self.get_ranking()[2] and self.get_ranking()[1] < y < self.get_ranking()[3]:
            game_framework.change_mode(ranking_mode)
        elif self.get_back()[0] < x < self.get_back()[2] and self.get_back()[1] < y < self.get_back()[3]:
            game_framework.change_mode(title_mode)


    def get_start(self):
        return 200, 260, 400, 320


    def get_practice(self):
        return 200, 370, 400, 430

    def get_back(self):
        return 0, 550, 100, 600

    def get_ranking(self):
        return 160, 180, 440, 120

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
                sel.check_click(event.x, 600 - 1 - event.y)
                pass
    pass


def init():
    global sel

    sel = Selectmode()
    game_world.add_object(sel, 0)
    pass

def finish():
    game_world.clear()
    pass

def update():
    game_world.update()
    pass

def draw():
    pico2d.clear_canvas()
    game_world.render()
    pico2d.update_canvas()
    pass



