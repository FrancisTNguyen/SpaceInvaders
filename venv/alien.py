import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    # a class to represent a single alien in the fleet

    def __init__(self, ai_settings, screen, alientype):
        # initialize the alien and get its starting position
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load the alien image and set its rect attribute
        self.image = pygame.image.load('alien' + str(alientype) + '.png')
        self.rect = self.image.get_rect()

        # start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the alien's exact location
        self.x = float(self.rect.x)

    def check_edges(self):
        # Return true if alien is at edge of the screen
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def blitme(self):
        # draw the alien at its current location
        self.screen.blit(self.image, self.rect)

    def update(self):
        # Move alien right
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
