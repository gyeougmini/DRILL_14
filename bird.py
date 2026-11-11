from pico2d import load_image


class Bird:
    image = None

    def __init__(self, x=800, y=400):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y

    def update(self):
        pass

    def draw(self):
        # 우선 스프라이트 시트 전체를 그려 이미지 로드를 확인
        Bird.image.draw(self.x, self.y)
