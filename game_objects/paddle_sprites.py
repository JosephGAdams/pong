import pygame

class paddle_sprite(pygame.sprite.Sprite):
    def __init__(self, size, colour, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.speed = 10