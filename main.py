import pygame
from pygame import mixer
import csv
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, BG, FPS, FONT_SIZE, PANEL, WHITE, PAD_SPEED, BRICK_WIDTH,\
    BRICK_HEIGHT, RED, BUTTON_WIDTH
from gameobjects import Pad, Ball, Brick

mixer.init()
pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Atari Breakout 1976")

clock = pygame.time.Clock()

level = 1
number_of_lives = 1
score = 0
game_over = True
next_level = False
new_game = False
read_name = True
user_name = ""

# pad movement variables
move_left = False
move_right = False


font = pygame.font.Font("assets/fonts/AtariClassic.ttf", FONT_SIZE)
large_font = pygame.font.Font("assets/fonts/AtariClassic.ttf", FONT_SIZE * 2)

def draw_text(x, y, font, text, color):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def scale_image(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

# load images

brick_types = 4
number_of_images = 2

ball_image = scale_image(pygame.image.load("assets/images/ball.png").convert_alpha(), 0.15)
pad_image = scale_image(pygame.image.load("assets/images/pad.png").convert_alpha(), 1)
button_image = scale_image(pygame.image.load("assets/images/1_0.png").convert_alpha(), 0.5)


all_brick_images = []
for i in range(brick_types):
    brick_images = []
    for j in range(number_of_images):
        brick_image = scale_image(pygame.image.load(f"assets/images/{i + 1}_{j}.png").convert_alpha(), 0.26)
        brick_images.append(brick_image)
    all_brick_images.append(brick_images)



# pygame.mixer.music.load("assets/audio/music.wav")
# pygame.mixer.music.set_volume(0.2)
# pygame.mixer.music.play(-1, 0.0, 5000)

# load sounds
brick_hit_sound = pygame.mixer.Sound("assets/audio/BrickHit.wav")
brick_hit_sound.set_volume(0.5)

wall_hit_sound = pygame.mixer.Sound("assets/audio/WallBounce.wav")
wall_hit_sound.set_volume(0.5)

pad_hit_sound = pygame.mixer.Sound("assets/audio/PadBounce.wav")
pad_hit_sound.set_volume(0.5)


def draw_main_menu_screen():
    draw_text(SCREEN_WIDTH//2 - 160, SCREEN_HEIGHT // 2 - 60, large_font, "BREAKOUT 1976", RED)
    button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, 65)
    button_rect.center = (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT // 2 + 60)
    screen.blit(button_image, button_rect)
    pygame.draw.rect(screen, RED, button_rect, 1)
    draw_text(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 50, font, "START", WHITE)
    return button_rect



def draw_game_info():
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 40))
    pygame.draw.line(screen, WHITE, (0, 40), (SCREEN_WIDTH, 40))
    # game info
    draw_text(10, 10, font, f"Score:{score}", WHITE)
    draw_text(SCREEN_WIDTH // 2 - 80, 10, font, f"Level:{level}", WHITE)
    draw_text(SCREEN_WIDTH - 160, 10, font, f"Lives: {number_of_lives}", WHITE)



def draw_game_over_screen():
    draw_text(SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 - 83, large_font, "GAME OVER!", WHITE)
    draw_text(SCREEN_WIDTH//2 - 160, SCREEN_HEIGHT // 2 - 80, large_font, "GAME OVER!", RED)
    draw_text(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 40, font, f"SCORE: {score}", RED)
    draw_text(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 20, font, f"LEVEL: {level}", RED)
    start_button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, 65)
    start_button_rect.center = (SCREEN_WIDTH//2 - 20, SCREEN_HEIGHT // 2 + 40)
    screen.blit(button_image, start_button_rect)
    pygame.draw.rect(screen, RED, start_button_rect, 1)
    draw_text(SCREEN_WIDTH // 2 - 55, SCREEN_HEIGHT // 2 + 30, font, "PLAY", WHITE)

    quit_button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, 65)
    quit_button_rect.center = (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 + 120)
    screen.blit(button_image, quit_button_rect)
    pygame.draw.rect(screen, RED, quit_button_rect, 1)
    draw_text(SCREEN_WIDTH // 2 - 55, SCREEN_HEIGHT // 2 + 110, font, "QUIT", WHITE)
    return start_button_rect, quit_button_rect

def draw_user_name():
    draw_text(SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 - 120, large_font, user_name, WHITE)

# Game objects
pad = Pad(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 15, pad_image)
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, ball_image)
bricks = pygame.sprite.Group()

def generate_level():
    # level generation logic
    with open(f"assets/levels/{level}.txt") as level_file:
        line = level_file.readline()
        row_counter = 0
        while line:
            if len(line) > 0:
                brick_types = line.split(",")
                counter = 0
                for brick_type in brick_types:
                    int_brick_value = int(brick_type)
                    if int_brick_value != 0:
                        brick = Brick(all_brick_images[int_brick_value - 1], \
                                      50 + counter * BRICK_WIDTH, 60 + BRICK_HEIGHT * row_counter, int_brick_value)
                        bricks.add(brick)
                    counter += 1
            row_counter += 1
            line = level_file.readline()


generate_level()


# Main game loop
run = True

while run:
    # control game speed
    clock.tick(FPS)

    # clearing the screen
    screen.fill(BG)

    if new_game:
        button_rect = draw_main_menu_screen()
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(pos[0], pos[1]):
                new_game = False
                number_of_lives = 3
                level = 1
                score = 0
    if game_over:
        draw_user_name()
        start_button_rect, quit_button_rect = draw_game_over_screen()
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if start_button_rect.collidepoint(pos[0], pos[1]):
                game_over = False
                number_of_lives = 3
                level = 1
                score = 0
            if quit_button_rect.collidepoint(pos[0], pos[1]):
                game_over = False
                run = False
    if not game_over:
        # check if next level achieved
        if next_level:
            next_level = False
            level += 1
            bricks = pygame.sprite.Group()
            generate_level()
            pad = Pad(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 15, pad_image)
            ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, ball_image)

        draw_game_info()

        # Calculate pad movements
        dx = 0

        if move_right:
            dx = PAD_SPEED
        if move_left:
            dx = -PAD_SPEED


        # Move game objects
        pad.move(dx)
        score_increment, off_screen_bottom, off_screen_top = ball.move(pad, bricks, brick_hit_sound, pad_hit_sound, wall_hit_sound)
        score += score_increment

        if off_screen_bottom:
            if number_of_lives > 0:
                number_of_lives -= 1
                ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, ball_image)
            else:
                # game over
                game_over = True
        if off_screen_top:
            next_level = True

        # Draw game objects
        pad.draw(screen)
        ball.draw(screen)

        for brick in bricks:
            brick.draw(screen)
    else:
        start_button_rect =  draw_game_over_screen()
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if start_button_rect.collidepoint(pos[0], pos[1]):
                game_over = False
                number_of_lives = 3
                level = 1
                score = 0


    # Event handling section
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False


        if event.type == pygame.KEYDOWN:
            if read_name:
                user_name += str(event.unicode).upper()
            else:
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
