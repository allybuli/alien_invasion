import pygame.font


class Button():

    def __init__(self,ai_settings,screen,msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 按键属性
        self.width = 200
        self.heigth = 50
        self.button_color = (0,255,233)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48)  # None表示使用默认字体

        # 创建按键的rect对象，并居中
        self.rect = pygame.Rect(0,0,self.width,self.heigth)
        self.rect.center = self.screen_rect.center

        # msg按钮显示的字体
        self.prep_msg(msg)

    def prep_msg(self,msg):
        # 将msg渲染为图像，并在按钮里居中
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 先绘制按钮再绘制文本
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)