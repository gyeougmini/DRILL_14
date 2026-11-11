import random

from pico2d import load_image, get_canvas_width, get_canvas_height

import game_framework

# 화면 단위 : 10 pixel = 30 cm (ruler.png 와 동일한 기준)
PIXEL_PER_METER = (10.0 / 0.3)

# 비행 속도 범위 (실제 소형~중형 조류의 순항 속도 수준)
FLY_SPEED_KMPH_MIN = 20.0
FLY_SPEED_KMPH_MAX = 40.0

# bird_animation.png : 918 x 506, 5열 x 3행 격자, 실제 프레임은 5 + 5 + 4 = 14장
FRAME_WIDTH = 183
FRAME_HEIGHT = 168
SHEET_HEIGHT = 506
FRAMES_PER_ROW = 5
FRAMES_PER_ACTION = 14

# 화면에 그릴 새의 실제 크기 (가로 2.0 m, 세로는 원본 비율 유지)
BIRD_WIDTH_M = 2.0
BIRD_WIDTH_PIXEL = BIRD_WIDTH_M * PIXEL_PER_METER
BIRD_HEIGHT_PIXEL = BIRD_WIDTH_PIXEL * FRAME_HEIGHT / FRAME_WIDTH


def kmph_to_pps(kmph):
    mpm = kmph * 1000.0 / 60.0      # km/h -> m/min
    mps = mpm / 60.0                # m/min -> m/s
    return mps * PIXEL_PER_METER    # m/s -> pixel/s

# 날갯짓 1회(14프레임)에 걸리는 시간
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_SECOND = FRAMES_PER_ACTION * ACTION_PER_TIME


class Bird:
    image = None

    def __init__(self):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        half_w, half_h = BIRD_WIDTH_PIXEL / 2, BIRD_HEIGHT_PIXEL / 2
        # 소년/땅과 겹치지 않도록 화면 위쪽 하늘 영역에 무작위 배치
        self.x = random.uniform(half_w, get_canvas_width() - half_w)
        self.y = random.uniform(250, get_canvas_height() - half_h)
        # 시작 프레임과 방향을 무작위로 하여 10마리가 똑같이 움직이지 않도록 함
        self.frame = random.uniform(0, FRAMES_PER_ACTION)
        self.dir = random.choice([-1, 1])    # 1: 오른쪽, -1: 왼쪽
        # 새마다 비행 속도를 다르게 함
        speed_kmph = random.uniform(FLY_SPEED_KMPH_MIN, FLY_SPEED_KMPH_MAX)
        self.speed_pps = kmph_to_pps(speed_kmph)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_SECOND * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.dir * self.speed_pps * game_framework.frame_time

        # 화면 끝에 닿으면 방향을 바꿔 좌우로 반복 비행
        half_w = BIRD_WIDTH_PIXEL / 2
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
        # 원본 이미지는 오른쪽을 바라보므로, 왼쪽으로 날 때는 'h' 로 좌우 반전
        flip = '' if self.dir == 1 else 'h'
        Bird.image.clip_composite_draw(left, bottom, FRAME_WIDTH, FRAME_HEIGHT,
                                       0, flip, self.x, self.y,
                                       BIRD_WIDTH_PIXEL, BIRD_HEIGHT_PIXEL)
