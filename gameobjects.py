import pygame
from constants import RED, SCREEN_WIDTH, PAD_SIZE, BALL_SPEED, BALL_WIDTH, BRICK_WIDTH, BRICK_HEIGHT

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
        self.rect = pygame.Rect(0, 0, BALL_WIDTH, BALL_WIDTH)
        self.rect.center = (x, y)
        self.dx = -BALL_SPEED
        self.dy = BALL_SPEED

    def move(self, pad: Pad, bricks):

        # check collision
        if self.rect.colliderect(pad.rect):
            self.dy = -self.dy

        # check if the ball goes of the screen
        if self.rect.x <= 0 or self.rect.x + BALL_WIDTH >= SCREEN_WIDTH:
            self.dx = -self.dx

        self.rect.y += self.dy

        # check for collisions with bricks
        for brick in bricks:
            if self.rect.colliderect(brick):
                if self.dy < 0:
                    # ball hits brick from the bottom
                    self.rect.top = brick.rect.bottom
                else:
                    # ball hits brick from the top
                    self.rect.bottom = brick.rect.top

                self.dy = -self.dy

        self.rect.x += self.dx
        # check for collisions with bricks
        for brick in bricks:
            if self.rect.colliderect(brick):
                if self.dx > 0:
                    # ball hits brick from the left side
                    self.rect.right = brick.rect.left

                else:
                    # ball hits brick from the right side
                    self.rect.left = brick.rect.right
                self.dx = -self.dx













    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, RED, self.rect, 1)


class Brick:

    def __init__(self, image, x, y):
        self.image = image
        self.rect = pygame.Rect(0, 0, BRICK_WIDTH, BRICK_HEIGHT)
        self.rect.center = (x, y)


    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, RED, self.rect, 1)
