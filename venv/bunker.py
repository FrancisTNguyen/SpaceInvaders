import pygame
from pygame.sprite import Sprite


class Bunker(Sprite):
    # a class that represents a single bunker
    def __init__(self, ai_settings, screen):
        # initialize the bunker and set starting position
        super(Bunker, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load bunker image and set its attributes
        self.image = pygame.image.load('Bunker.png')
        self.rect = self.image.get_rect()

        # set location for new bunker
        self.rect.x = self.rect.width
        self.rect.y = 600

        # store bunker location
        self.x = float(self.rect.x)

    def blitme(self):
        # draw bunker at current location
        self.screen.blit(self.image, self.rect)
