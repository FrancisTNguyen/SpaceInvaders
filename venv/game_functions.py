import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
from bunker import Bunker

# set theme music
pygame.mixer.init()
pygame.mixer_music.load('defaulttheme.wav')
pygame.mixer_music.set_volume(0.5)
pygame.mixer_music.play(-1)

# set sound effects
shoot_effect = pygame.mixer.Sound('shipshoot.ogg')
explosion_effect = pygame.mixer.Sound('alienexplosion.ogg')
explosion_effect.set_volume(0.5)
lose_effect = pygame.mixer.Sound('shiplose.ogg')


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers):
    # respond to ship behing hit by aliens
    lose_effect.play()
    if stats.ships_left > 0:
        # decrement ships left
        stats.ships_left -= 1

        # update scoreboard
        sb.prep_ships()

        # empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        bunkers.empty()

        # create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        create_row_bunkers(ai_settings, screen, bunkers)
        ship.center_ship()

        # pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # Respond to keypresses and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    # start a new game when the player clicks Play
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings
        ai_settings.initialize_dynamic_settings()

        # hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Reset the game stats
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    # responds to keypresses
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        shoot_effect.play()
        fire_bullet(ai_settings, screen, ship, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    # Fire a bullet if limit not reached yet
    # create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    # respond to key releases
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_fleet_edges(ai_settings, aliens):
    # Respond appropriately if any aliens have reached an edge
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    # Drop the entire fleet and change the fleet's direction
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def get_number_aliens_x(ai_settings, alien_width):
    # Determine the number of aliens that fit in a row
    available_space_x = ai_settings.screen_width - 1.5 * alien_width
    number_aliens_x = int(available_space_x / (1.5 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    # Determine the number of rows of aliens that fit on the screen
    available_space_y = (ai_settings.screen_height - (1.5 * alien_height) - ship_height)
    number_rows = int(available_space_y / (1.5 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # Create an alien and place it in the room
    if int(row_number) == 0:
        alien = Alien(ai_settings, screen, 3, )
    if int(row_number) == 1:
        alien = Alien(ai_settings, screen, 3)
    if int(row_number) == 2:
        alien = Alien(ai_settings, screen, 1)
    if int(row_number) == 3:
        alien = Alien(ai_settings, screen, 1)
    if int(row_number) == 4:
        alien = Alien(ai_settings, screen, 2)
    if int(row_number) == 5:
        alien = Alien(ai_settings, screen, 2)

    alien_width = alien.rect.width
    alien.x = alien_width + 1 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1 * alien.rect.height * row_number
    aliens.add(alien)


def create_bunker(ai_settings, screen, bunkers, num_bunker):
    bunker = Bunker(ai_settings, screen)
    bunker_width = bunker.rect.width
    bunker.x = bunker_width + 20
    bunker.rect.x = bunker.x + 2 * bunker_width * num_bunker - 50
    bunker.rect.y = bunker.rect.height + 2 * bunker.rect.height + 360
    bunkers.add(bunker)


def create_row_bunkers(ai_settings, screen, bunkers):
    num_bunkers = 6

    for collumn_bunkers in range(num_bunkers):
        create_bunker(ai_settings, screen, bunkers, collumn_bunkers)


def create_fleet(ai_settings, screen, ship, aliens):
    # create a full fleet of aliens
    # create an alien and find the number of aliens in a row
    alien = Alien(ai_settings, screen, 1)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Create an alien and place it in the row
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, bunkers, hs_button):
    # update images on the screen and flip to new screen
    screen.fill(ai_settings.bg_color)

    # redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    bunkers.draw(screen)

    # Draw the score information
    sb.show_score()

    # Draw the play button if the game is inactive
    if not stats.game_active:
        screen.fill(ai_settings.start_color)
        font = pygame.font.SysFont(None, 100)
        screen_text = font.render("Space Invaders", True, (255, 255, 255))
        screen.blit(screen_text, [ai_settings.screen_width - 850, 50])
        play_button.draw_button()
        hs_button.draw_button_hs()

    # make the most recently drawn screen visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers):
    # Update position of bullets and get reid of old bullets
    # Update bullet positions
    bullets.update()

    collisions = pygame.sprite.groupcollide(bullets, bunkers, True, True)

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        if collisions:
            explosion_effect.play()
            for bunkers in collisions.values():
                bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers):
    # check for any bullets that have hit aliens
    # if so get rid of the bullet and the alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            explosion_effect.play()
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # if the entire fleet is destroyed, start a new level
        bullets.empty()
        ai_settings.increase_speed()

        # increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)
        create_row_bunkers(ai_settings, screen, bunkers)


def check_aliens_bunkers_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers):
    # check for the collisions between aliens and bunkers
    collisions = pygame.sprite.groupcollide(aliens, bunkers, True, True)

    if collisions:
        for bunkers in collisions.values():
            explosion_effect.play()
            stats.score += ai_settings.alien_points * len(aliens)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # check if any aliens have reached the bottom of screen
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # treat this the same as if the ship got hit
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers)
            break


def check_high_score(stats, sb):
    # check to see if there's a new high score
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers):
    # check if the fleet is at an edge, and then update the positions of all aliens in the fleet
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers)

    # Look for alien hitting the bottom of the screen
    check_aliens_bunkers_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers)
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
