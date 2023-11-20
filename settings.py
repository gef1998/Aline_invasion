
class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""

    def __init__(self):
        """初始化游戏的设置。"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        self.ship_speed = 1.0


        self.bullet_speed = 1.0
        self.bullets_allowed = 5

        self.alien_speed = 0.8
        self.fleet_drop_speed = 50

        self.ship_limit = 1

