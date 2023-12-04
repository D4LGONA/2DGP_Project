from pico2d import *
import game_framework
import game_world
import select_mode

# Todo: 파일 입출력 해서 데이터 리스트에 넣기

class Ranking:
    def __init__(self):
        self.image = load_image('resources/ranking.png')
        self.cx = 300
        self.cy = 300
        self.font = self.font = load_font('ENCR10B.TTF', 16)

    def draw(self):
        self.image.draw(300, 300, 600, 600)

    def update(self):
        pass

def init():
    global rank
    rank = Ranking()
    game_world.add_object(rank, 4)
    pass

def finish():
    game_world.remove_object(rank)
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
                    game_framework.change_mode(select_mode)
    pass

