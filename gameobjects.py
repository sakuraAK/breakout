import pygame
from constants import RED, SCREEN_WIDTH, PAD_SIZE

class Pad:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = pygame.Rect(0, 0, PAD_SIZE, 15)
        self.rect.center = (x, y)


    def move(self, dx):

        # Test for screen boundaries

        # Reached left side

        tmp_x = self.rect.x
        tmp_x += dx
        if tmp_x <= 0:
            self.rect.x = 0
            return

        # Reached right side

        tmp_x = self.rect.x
        tmp_x = tmp_x + dx + PAD_SIZE
        if tmp_x >= SCREEN_WIDTH:
            self.rect.x = SCREEN_WIDTH - PAD_SIZE
            return


        self.rect.x += dx


    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, RED, self.rect, 1)


class Ball:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = pygame.Rect(0, 0, 15, 15)
        self.rect.center = (x, y)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, RED, self.rect, 1)