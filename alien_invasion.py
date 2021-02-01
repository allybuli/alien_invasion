import pygame

from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()

    # 创建窗体，一个surface
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建按钮
    play_button = Button(ai_settings,screen,"Play")

    # 创建飞船
    ship = Ship(ai_settings,screen)
    # 创建存储子弹的编组
    bullets = Group()

    # 创建存储外星人的编组
    aliens = Group()
    # 创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)
    # 创建一个实例存储统计信息
    stats = GameStats(ai_settings)
    # 创建记分牌
    sb = Scoreboard(ai_settings,screen,stats)
    # 开始游戏
    while True:
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            ship.update()

            # 删除消失的子弹以及击中外星人的子弹和被击中的外星人
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)

            gf.update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets)

        gf.update_screen(ai_settings, screen, stats,sb,ship,aliens,bullets,play_button)


run_game()