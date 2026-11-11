from pico2d import load_image

# bird_animation.png : 918 x 506, 5열 x 3행 격자
FRAME_WIDTH = 183
FRAME_HEIGHT = 168
SHEET_HEIGHT = 506


class Bird:
    image = None

    def __init__(self, x=800, y=400):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.frame = 0

    def update(self):
        pass

    def draw(self):
        # 첫 번째 프레임(맨 윗줄, 맨 왼쪽)만 그린다
        bottom = SHEET_HEIGHT - FRAME_HEIGHT
        Bird.image.clip_draw(0, bottom, FRAME_WIDTH, FRAME_HEIGHT, self.x, self.y)
