import pygame
from pygame import mixer
import csv
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, BG, FPS, FONT_SIZE, PANEL, WHITE, PAD_SPEED, BALL_SPEED
from gameobjects import Pad, Ball

mixer.init()
pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Atari Breakout 1976")

clock = pygame.time.Clock()

# pad movement variables
move_left = False
move_right = False


font = pygame.font.Font("assets/fonts/AtariClassic.ttf", FONT_SIZE)

def draw_text(x, y, font, text, color):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def scale_image(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

# load images
ball_image = scale_image(pygame.image.load("assets/images/ball.png").convert_alpha(), 1)
pad_image = scale_image(pygame.image.load("assets/images/pad.png").convert_alpha(), 1)

# pygame.mixer.music.load("assets/audio/music.wav")
# pygame.mixer.music.set_volume(0.2)
# pygame.mixer.music.play(-1, 0.0, 5000)

# load sounds
brick_hit_sound = pygame.mixer.Sound("assets/audio/BrickHit.wav")
brick_hit_sound.set_volume(0.5)




def level_gen():
    with open(f"assets/levels/level_data.csv") as in_file:
       pass


def draw_game_info():
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 50))
    pygame.draw.line(screen, WHITE, (0, 50), (SCREEN_WIDTH, 50))
    # game info



# Game objects
pad = Pad(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 15, pad_image)
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, ball_image)



# Main game loop
run = True

while run:
    # control game speed
    clock.tick(FPS)

    # clearing the screen
    screen.fill(BG)

    # Calculate pad movements
    dx = 0

    if move_right:
        dx = PAD_SPEED
    if move_left:
        dx = -PAD_SPEED


    # Move game objects
    pad.move(dx)
    ball.move(BALL_SPEED, -BALL_SPEED)


    # Draw game objects
    pad.draw(screen)
    ball.draw(screen)


    # Event handling section
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            if event.key == pygame.K_RIGHT:
                move_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False

    # Render the display
    pygame.display.update()



pygame.quit()
