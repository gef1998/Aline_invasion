import pygame
from pygame.sprite import Sprite
from settings import Settings

class Alien(Sprite):
    """表示单个外星人的类。"""

    def __init__(self, ai_game):
        """初始化外星人并设置其起始位置。"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = Settings()
        # 加载外星人图像并设置其rect属性
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近。
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的精确水平位置。
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.fleet_direction = 1 # 1表示向右，-1表示向左


    def darw(self):
        """在指定位置绘制外星人。"""
        self.screen.blit(self.image, self.rect)

    def _update_fleet_direction(self):
        if self.x >= self.settings.screen_width - self.rect.width:
            self.fleet_direction = -1
            self.y += self.settings.fleet_drop_speed
        elif self.x <= 0:
            self.fleet_direction = 1
            self.y += self.settings.fleet_drop_speed

    def update(self):
        self._update_fleet_direction()
        
        if self.fleet_direction == 1:
            self.x += self.settings.alien_speed
        elif self.fleet_direction == -1:
            self.x -= self.settings.alien_speed

        self.rect.x = self.x
        self.rect.y = self.y