import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_settings,screen):
        super(Ship,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # 加载飞船图像并获取其外接矩阵
        self.image = pygame.image.load('images/ship.bmp')  # 飞船图像
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()               # 飞船图像的外接矩阵

        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx  # x坐标
        self.rect.bottom = self.screen_rect.bottom  # y坐标
        self.center = float(self.rect.centerx)

        self.moving_right = False  # 向右移动的标志
        self.moving_left = False  # 向左移动的标志

    def update(self):
        # 长摁一直移动
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_spead_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_spead_factor
        self.rect.centerx = self.center

    def center_ship(self):
        # 让飞船在屏幕上居中
        self.center = self.screen_rect.centerx

    def blitme(self):
        # 在指定位置绘制飞船
        self.screen.blit(self.image, self.rect)