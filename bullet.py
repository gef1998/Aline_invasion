import pygame
from pygame.sprite import Sprite
from settings import Settings

"""
下面来添加射击功能。我们将编写在玩家按空格键时发射子弹（用小矩形表示）的代码。
子弹将在屏幕中向上飞行，抵达屏幕上边缘后消失。
"""
class Bullet(Sprite):
    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置。"""
        super().__init__()
        self.settings = Settings()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.ai_game = ai_game
          # 加载飞船图像并获取其外接矩形。
        self.image = pygame.image.load('images/bullet.png')
        self.rect = self.image.get_rect()
          # 对于每艘新飞船，都将其放在屏幕底部的中央。
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def blit_bullet(self):
        """在指定位置绘制子弹。"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y