
import sys
import pygame
from bullet import Bullet
from alien import Alien
from random import randint

from settings import Settings
from ship import Ship

class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源。"""
        pygame.init()
        self.settings = Settings()
        fullscreen_choice  = input("全屏吗？(yes or no)").lower()
        assert fullscreen_choice in ['yes', 'no'], "无效的选项，请输入 'yes' 或 'no'"
        if fullscreen_choice == 'no':
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        if fullscreen_choice == 'yes':
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()


    def _check_events(self):
        """响应鼠标和按键事件。"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.KEYDOWN:         
                self._check_keydown_events(event)

    def _check_keyup_events(self, event): 
        """响应松开。"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_keydown_events(self, event):
        """响应按键。"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        """创建一颗子弹,并将其加入编组bullets中。"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """ 创建外星人群。"""
        alien = Alien(self)
        available_space_x = self.settings.screen_width - (2 * alien.rect.width)
        available_space_y = self.settings.screen_height - (3 * alien.rect.height) - self.ship.rect.height
        number_aliens_x = available_space_x // (2 * alien.rect.width)
        number_rows = available_space_y // (2 * alien.rect.height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(row_number, alien_number)

    def _create_alien(self, row_number ,alien_number):
        """创建一个外星人，并将其放在当前行。"""
        new_alien = Alien(self)
        # 在x轴位置上增加一个随机偏移量
        x_offset = randint(-10, 10)
        new_alien.x += alien_number * new_alien.rect.width * 2 + x_offset
        # 在y轴上设置外星人的位置
        new_alien.y += row_number * new_alien.rect.height * 2

        # 将计算得到的坐标赋值给外星人的矩形属性
        new_alien.rect.x = new_alien.x
        new_alien.rect.y = new_alien.y
        # 将新创建的外星人添加到外星人群组
        self.aliens.add(new_alien)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_aliens(self):
        self.aliens.update()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.aliens.draw(self.screen)

        for bullet in self.bullets.sprites():
            bullet.blit_bullet()
        # 让最近绘制的屏幕可见。
        pygame.display.flip()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 监视键盘和鼠标事件。
            self._check_events()
            self.ship.move()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏。
    ai = AlienInvasion()
    ai.run_game()