import pygame
from constants import RED, SCREEN_WIDTH, PAD_SIZE, BALL_SPEED, BALL_WIDTH, BRICK_WIDTH,\
    BRICK_HEIGHT, SCREEN_HEIGHT

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

    def move(self, pad: Pad, bricks, brick_hit_sound, pad_hit_sound, wall_hit_sound):
        off_screen_bottom = False
        off_screen_top = False
        s = set()

        # check if the ball goes of the screen bottom
        if self.rect.y >= SCREEN_HEIGHT:
            off_screen_bottom = True
        elif self.rect.y <= 40:
            off_screen_top = True
        else:
            # check collision
            if self.rect.colliderect(pad.rect):
                pad_hit_sound.play()
                self.dy = -self.dy


            # check if the ball hits the wall (left/right)
            if self.rect.x <= 0 or self.rect.x + BALL_WIDTH >= SCREEN_WIDTH:
                wall_hit_sound.play()
                self.dx = -self.dx

            self.rect.y += self.dy

            # check for collisions with bricks
            for brick in bricks:
                if self.rect.colliderect(brick):
                    if brick not in s:
                        brick_hit_sound.play()
                        brick.update_hit()
                        s.add(brick)

                    if self.dy < 0:
                        # ball hits brick from the bottom
                        self.rect.top = brick.rect.bottom
                    else:
                        # ball hits brick from the top
                        self.rect.bottom = brick.rect.top

                    self.dy = -self.dy

                    # update brick got hit



            self.rect.x += self.dx
            # check for collisions with bricks
            for brick in bricks:
                if self.rect.colliderect(brick):
                    if brick not in s:
                        brick_hit_sound.play()
                        brick.update_hit()
                        s.add(brick)
                    if self.dx > 0:
                        # ball hits brick from the left side
                        self.rect.right = brick.rect.left

                    else:
                        # ball hits brick from the right side
                        self.rect.left = brick.rect.right
                    self.dx = -self.dx

        return len(s), off_screen_bottom, off_screen_top


    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, RED, self.rect, 1)


class Brick(pygame.sprite.Sprite):

    def __init__(self, images, x, y, brick_type):
        pygame.sprite.Sprite.__init__(self)
        self.brick_type = brick_type
        self.images = images
        self.rect = pygame.Rect(0, 0, BRICK_WIDTH, BRICK_HEIGHT)
        self.rect.center = (x, y)
        self.hit_counter = 0

    def update_hit(self):
        if self.hit_counter == 0:
            self.hit_counter += 1
        else:
            self.kill()

    def draw(self, surface):
        surface.blit(self.images[self.hit_counter], self.rect)
        pygame.draw.rect(surface, RED, self.rect, 1)
