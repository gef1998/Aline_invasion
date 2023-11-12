
import sys
import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源。"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_height, self.settings.screen_width))
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)


    def _check_events(self):
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
            elif event.type == pygame.KEYDOWN:         
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True                            

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()      
        # 让最近绘制的屏幕可见。
        pygame.display.flip()
        


    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 监视键盘和鼠标事件。
            self._check_events()
            self.ship.move()
            self._update_screen()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏。
    ai = AlienInvasion()
    ai.run_game()