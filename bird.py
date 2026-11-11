from pico2d import load_image

# bird_animation.png : 918 x 506, 5열 x 3행 격자, 실제 프레임은 5 + 5 + 4 = 14장
FRAME_WIDTH = 183
FRAME_HEIGHT = 168
SHEET_HEIGHT = 506
FRAMES_PER_ROW = 5
FRAMES_PER_ACTION = 14


class Bird:
    image = None

    def __init__(self, x=800, y=400):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.frame = 0.0

    def update(self):
        pass

    def draw(self):
        index = int(self.frame)
        col = index % FRAMES_PER_ROW
        row = index // FRAMES_PER_ROW          # 0: 맨 윗줄
        left = col * FRAME_WIDTH
        bottom = SHEET_HEIGHT - (row + 1) * FRAME_HEIGHT   # pico2d 는 아래쪽이 y=0
        Bird.image.clip_draw(left, bottom, FRAME_WIDTH, FRAME_HEIGHT, self.x, self.y)
