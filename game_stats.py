class GameStats():  # 统计信息类

    def __init__(self,ai_settings):
        self.ai__settings = ai_settings
        self.reset_stats()
        # 最高得分不重置
        self.high_score = 0

        # 让游戏一开始处于非活动状态
        self.game_active = False

    def reset_stats(self):
        self.ships_left = self.ai__settings.ship_limit
        self.score = 0  # 当前得分
        self.level = 1  # 第几波外星人