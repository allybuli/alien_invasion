import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien
from scoreboard import Scoreboard

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:  # 向右移动
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:  # 向左移动
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:  # 空格键
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:  # 摁q键结束游戏
        sys.exit()


def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    # 响应按键和鼠标
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 关闭窗口
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # 摁下按键
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:  # 松开按键
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()  # 获取鼠标单击的位置
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)


def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    # 单击按钮开始新游戏
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active :  # 鼠标单击的位置在按钮内
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        # 重置剩余飞船数
        sb.prep_ships()
        # 清空外星人和子弹
        aliens.empty()
        bullets.empty()
        # 创建一波新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats,sb,ship,aliens,bullets,play_button):
    # 更新 新屏幕新图像
    screen.fill(ai_settings.bg_color)
    # 重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)  # 绘制编组中的每一个外星人
    # 显示得分
    sb.show_score()
    # 让最近绘制的屏幕可见
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):

    # 更新子弹位置
    bullets.update()
    # 删除消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # 检测是否有子弹击中了外星人
    check_bullet_alien_collisions(ai_settings, screen,stats,sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    # 删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)  # collisions是一个字典
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats, sb)
    # 在一波攻击中，消灭所有外星人后，删除现有的子弹,并生成下一波外星人,并提高一个等级
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def update_aliens(ai_settings, stats,sb,screen,ship, aliens,bullets):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    # 检测外星人和飞船的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
    # 检查是否有外星人到达了外星人到达了屏幕底部
    check_aliens_bottom(ai_settings, stats, sb,screen, ship, aliens, bullets)


def fire_bullet(ai_settings, screen, ship,bullets):  # 发射子弹
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_settings,screen,ship,aliens):  # 创建外星人群
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)


def create_alien(ai_settings,screen,aliens,alien_number,row_number):  # 创建一个外星人
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number  # 该外星人的x坐标
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)


def get_number_aliens_x(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))  # 屏幕一行可放置外星人的数目
    return number_aliens_x


def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y = ai_settings.screen_height - (3*alien_height) - ship_height
    number_rows = int(available_space_y / (2*alien_height))
    return number_rows


def check_fleet_edges(ai_settings,aliens):

    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break


def change_fleet_direction(ai_settings,aliens):

    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_spead
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets):
    # 响应被外星人撞到的飞船,飞船数目减1
    if stats.ships_left > 0:
        stats.ships_left -= 1
        # 更新记分牌
        sb.prep_ships()
        # 清空外星人和子弹
        aliens.empty()
        bullets.empty()

        # 创建一波新的外星人，并将飞船放到屏幕底中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets):
    # 检查是否有外星人到达了外星人到达了屏幕底部
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats,sb, screen, ship, aliens, bullets)
            break


def check_high_score(stats,sb):
    # 更新最高得分
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()