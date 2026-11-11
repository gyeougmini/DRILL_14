from pico2d import load_image

import game_framework

# 화면 단위 : 10 pixel = 30 cm (ruler.png 와 동일한 기준)
PIXEL_PER_METER = (10.0 / 0.3)

# 비행 속도 : km/h -> m/min -> m/s -> pixel/s
FLY_SPEED_KMPH = 30.0
FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)

# bird_animation.png : 918 x 506, 5열 x 3행 격자, 실제 프레임은 5 + 5 + 4 = 14장
FRAME_WIDTH = 183
FRAME_HEIGHT = 168
SHEET_HEIGHT = 506
FRAMES_PER_ROW = 5
FRAMES_PER_ACTION = 14

# 날갯짓 1회(14프레임)에 걸리는 시간
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_SECOND = FRAMES_PER_ACTION * ACTION_PER_TIME


class Bird:
    image = None

    def __init__(self, x=800, y=400):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.frame = 0.0
        self.dir = 1    # 1: 오른쪽, -1: 왼쪽

    def update(self):
        self.frame = (self.frame + FRAMES_PER_SECOND * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.dir * FLY_SPEED_PPS * game_framework.frame_time

    def draw(self):
        index = int(self.frame)
        col = index % FRAMES_PER_ROW
        row = index // FRAMES_PER_ROW          # 0: 맨 윗줄
        left = col * FRAME_WIDTH
        bottom = SHEET_HEIGHT - (row + 1) * FRAME_HEIGHT   # pico2d 는 아래쪽이 y=0
        Bird.image.clip_draw(left, bottom, FRAME_WIDTH, FRAME_HEIGHT, self.x, self.y)
