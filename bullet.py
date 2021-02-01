import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):

    def __init__(self,ai_settings,screen,ship):
        super(Bullet, self).__init__()

        self.screen = screen

        # 创建子弹，并放到正确的位置
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top  # 子弹从飞船顶部射出

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.spead_factor = ai_settings.bullet_spead_factor

    def update(self):
        # 子弹向上移动
        self.y -= self.spead_factor
        self.rect.y = self.y

    def draw_bullet(self):
        # 在屏幕上绘制子弹
        pygame.draw.rect(self.screen,self.color,self.rect)
