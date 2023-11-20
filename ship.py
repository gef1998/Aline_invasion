import pygame
from settings import Settings


class Ship:
    """管理飞船的类"""
    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置。"""
        self.settings = Settings()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.ai_game = ai_game
          # 加载飞船图像并获取其外接矩形。
        self.image = pygame.image.load('images/ship.jpg')
        self.rect = self.image.get_rect()
          # 对于每艘新飞船，都将其放在屏幕底部的中央。
        self.center_ship()
        self.moving_right = False
        self.moving_left = False
        
    def blitme(self):
        """在指定位置绘制飞船。"""
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """让飞船在屏幕底端居中。"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def move(self):
        if self.moving_right:
            self.x += self.settings.ship_speed
        if self.moving_left:
            self.x -= self.settings.ship_speed
        self.x = max(0, min(self.x, self.screen_rect.right - self.rect.width))
        self.rect.x = self.x    
