
import sys
import pygame


from bullet import Bullet
from alien import Alien
from random import randint
from time import sleep
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button

class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源。"""
        pygame.init()
        self.settings = Settings()
        self.stats = GameStats(self)
        if not self.settings.is_fullscreen:
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Play")
        self.fullscreen_button = Button(self, "fullscreen")
        self.fullscreen_button.msg_image_rect.y -= 100
        self.fullscreen_button.rect.y -= 100
        self.clock = pygame.time.Clock()

    def _check_events(self):
        """响应鼠标和按键事件。"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.KEYDOWN:         
                self._check_keydown_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 难道不应该是按下时按钮变形，鼠标松开时判断鼠标是否在坐标内吗？ 还有开始游戏后继续鼠标点击按钮区域还是会进行判断
                mouse_pos = pygame.mouse.get_pos()
                self._check_button(mouse_pos)

    def _check_button(self, mouse_pos):
        """在玩家单击Play按钮时开始新游戏。
           在玩家单击fullscreen按钮时全屏。
        """
        play_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        fullscreen_button_clicked = self.fullscreen_button.rect.collidepoint(mouse_pos)
        if play_button_clicked and not self.stats.game_active:
            self.stats.game_active = True
            pygame.mouse.set_visible(False)
        if fullscreen_button_clicked and not self.stats.game_active:
            Settings.is_fullscreen = True
            self.__init__()

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
        available_space_x = self.screen_rect.width - (2 * alien.rect.width)
        available_space_y = self.screen_rect.height - (3 * alien.rect.height) - self.ship.rect.height
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

        collitions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)        
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        self._check_aliens_bottom()
                   
    def _ship_hit(self):
        """响应飞船被外星人撞到。"""
        if self.stats.ships_left <= 0:
             self.stats.game_active = False
             pygame.mouse.set_visible(True)
             return
        # 将ships_left减1。
        self.stats.ships_left -= 1

            # 清空余下的外星人和子弹。
        self.aliens.empty()
        self.bullets.empty()

            # 创建一群新的外星人，并将飞船放到屏幕底端的中央。
        self._create_fleet()
        self.ship.center_ship()

            # 暂停。
        sleep(0.5)
    
    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端。"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞到一样处理。
                self._ship_hit()
                break

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.fullscreen_button.draw_button()
        else:
            self.ship.blitme()
            self.aliens.draw(self.screen)
            for bullet in self.bullets.sprites():
                bullet.blit_bullet()
        # 让最近绘制的屏幕可见。
        pygame.display.flip()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self.clock.tick(144)
            # 监视键盘和鼠标事件。
            self._check_events()
            if self.stats.game_active:
                self.ship.move()
                self._update_bullets()
                self._update_aliens()   # 天呐，我发现外星人越少他移动速度越快！
            self._update_screen()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏。
    ai = AlienInvasion()
    ai.run_game()