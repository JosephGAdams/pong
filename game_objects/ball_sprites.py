import pygame

class ball_sprite(pygame.sprite.Sprite):
    def __init__(self, size, position, colour, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        pygame.draw.circle(self.image, colour, (size[0]/2, size[1]/2), 5, 0)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position[0], position[1]
        self.x_speed = 5
        self.y_speed = 5    
        self.x_direction = "right"
        self.y_direction = "up"