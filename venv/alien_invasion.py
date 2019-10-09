import sys
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from hs_buttom import HSButton
from ship import Ship
from alien import Alien
from bunker import Bunker
import game_functions as gf
from pygame.sprite import Group


def run_game():
    # initialize py-game, settings, and screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the play button
    play_button = Button(ai_settings, screen, "Play")
    hs_button = HSButton(ai_settings, screen, "High Score")

    # Create an instance to store game stats and create a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # make a ship variable that accesses the ship class
    ship = Ship(ai_settings, screen)

    # make groups to store bullets in and a group of aliens
    bullets = Group()
    aliens = Group()
    bunkers = Group()

    # create the fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # create row of bunkers
    gf.create_row_bunkers(ai_settings, screen, bunkers)

    # start the main loop for the game
    while True:

        # watch for keyboard or mouse events
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, bunkers)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, bunkers, hs_button)


run_game()
