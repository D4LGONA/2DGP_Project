from pico2d import *
import game_framework
import game_world
import play_mode
import seesaw_mode
import select_mode
import huddle_mode
import a_frame_mode
import tunnel_mode
import weavepoles_mode


class Selectmode2:
    def __init__(self):
        self.image = load_image("resources/select_2.png")
        self.x, self.y = 300, 300

    def draw(self):
        self.image.draw(self.x, self.y, 600, 600)
        draw_rectangle(*self.get_huddle())
        draw_rectangle(*self.get_tunnel())
        draw_rectangle(*self.get_seesaw())
        draw_rectangle(*self.get_aframe())
        draw_rectangle(*self.get_weavepoles())
        draw_rectangle(*self.get_all())
        draw_rectangle(*self.get_back())

    def update(self):
        pass

    def check_click(self, x, y):
        if self.get_back()[0] < x < self.get_back()[2] and self.get_back()[1] < y < self.get_back()[3]:
            game_framework.change_mode(select_mode)
        elif self.get_huddle()[0] < x < self.get_huddle()[2] and self.get_huddle()[1] < y < self.get_huddle()[3]:
            game_framework.change_mode(huddle_mode)
        elif self.get_tunnel()[0] < x < self.get_tunnel()[2] and self.get_tunnel()[1] < y < self.get_tunnel()[3]:
            game_framework.change_mode(tunnel_mode)
        elif self.get_seesaw()[0] < x < self.get_seesaw()[2] and self.get_seesaw()[1] < y < self.get_seesaw()[3]:
            game_framework.change_mode(seesaw_mode)
        elif self.get_aframe()[0] < x < self.get_aframe()[2] and self.get_aframe()[1] < y < self.get_aframe()[3]:
            game_framework.change_mode(a_frame_mode)
        elif self.get_weavepoles()[0] < x < self.get_weavepoles()[2] and self.get_weavepoles()[1] < y < self.get_weavepoles()[3]:
            game_framework.change_mode(weavepoles_mode)
        elif self.get_all()[0] < x < self.get_all()[2] and self.get_all()[1] < y < self.get_all()[3]:
            game_framework.change_mode(play_mode)
            play_mode.is_recode = False
            pass

    def get_huddle(self):
        return 120, 380, 280, 440


    def get_tunnel(self):
        return 320, 380, 480, 440

    def get_seesaw(self):
        return 120, 280, 280, 340

    def get_aframe(self):
        return 320, 280, 480, 340

    def get_weavepoles(self):
        return 120, 180, 280, 240

    def get_all(self):
        return 320, 180, 480, 240

    def get_back(self):
        return 0, 550, 100, 600

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
                sel2.check_click(event.x, 600 - 1 - event.y)
                pass
    pass


def init():
    global sel2

    sel2 = Selectmode2()
    game_world.add_object(sel2, 0)
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



