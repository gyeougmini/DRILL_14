import random

from pico2d import load_image, get_canvas_width, get_canvas_height

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

    def __init__(self):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        half_w, half_h = FRAME_WIDTH // 2, FRAME_HEIGHT // 2
        # 소년/땅과 겹치지 않도록 화면 위쪽 하늘 영역에 무작위 배치
        self.x = random.randint(half_w, get_canvas_width() - half_w)
        self.y = random.randint(250, get_canvas_height() - half_h)
        # 시작 프레임과 방향을 무작위로 하여 10마리가 똑같이 움직이지 않도록 함
        self.frame = random.uniform(0, FRAMES_PER_ACTION)
        self.dir = random.choice([-1, 1])    # 1: 오른쪽, -1: 왼쪽

    def update(self):
        self.frame = (self.frame + FRAMES_PER_SECOND * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.dir * FLY_SPEED_PPS * game_framework.frame_time

        # 화면 끝에 닿으면 방향을 바꿔 좌우로 반복 비행
        half_w = FRAME_WIDTH // 2
        if self.x > get_canvas_width() - half_w:
            self.x = get_canvas_width() - half_w
            self.dir = -1
        elif self.x < half_w:
            self.x = half_w
            self.dir = 1

    def draw(self):
        index = int(self.frame)
        col = index % FRAMES_PER_ROW
        row = index // FRAMES_PER_ROW          # 0: 맨 윗줄
        left = col * FRAME_WIDTH
        bottom = SHEET_HEIGHT - (row + 1) * FRAME_HEIGHT   # pico2d 는 아래쪽이 y=0
        if self.dir == 1:
            # 원본 이미지는 오른쪽을 바라봄
            Bird.image.clip_draw(left, bottom, FRAME_WIDTH, FRAME_HEIGHT, self.x, self.y)
        else:
            # 왼쪽으로 날 때는 좌우 반전
            Bird.image.clip_composite_draw(left, bottom, FRAME_WIDTH, FRAME_HEIGHT,
                                           0, 'h', self.x, self.y, FRAME_WIDTH, FRAME_HEIGHT)
