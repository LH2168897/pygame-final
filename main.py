"""
Pygame Final: Pong
May 2026

Controls:
- Left Paddle: 'W' (Up), 'S' (Down)
- Right Paddle: Up Arrow, Down Arrow
"""

import sys
import random
import pygame


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
COLOR_BG = (30, 30, 40)       # Dark slate blue
COLOR_TEXT = (220, 220, 230)   # white
COLOR_ELEMENTS = (255, 255, 255) # White

# Game Object Dimensions
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 15

# Speeds
PADDLE_SPEED = 7
BALL_START_SPEED_X = 5
BALL_START_SPEED_Y = 5

# --- GAME SETUP ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Classic Pong - Final Project")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas", 60)

left_paddle = pygame.Rect(50, (SCREEN_HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(SCREEN_WIDTH - 50 - PADDLE_WIDTH, (SCREEN_HEIGHT // 2) - (PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect((SCREEN_WIDTH // 2) - (BALL_SIZE // 2), (SCREEN_HEIGHT // 2) - (BALL_SIZE // 2), BALL_SIZE, BALL_SIZE)

# Ball movement
ball_speed_x = BALL_START_SPEED_X * random.choice((1, -1))
ball_speed_y = BALL_START_SPEED_Y * random.choice((1, -1))

# Score tracking
left_score = 0
right_score = 0

# EASTER EGG VARIABLES
egg_start_time = 0
egg_triggered = False

try:
    egg_image = pygame.image.load("face/maxresdefault.jpg").convert()
    # Scale image to look good on screen
    egg_image = pygame.transform.scale(egg_image, (300, 300))
    egg_rect = egg_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
except pygame.error:
    # So the game dont kill itsself
    egg_image = None
    egg_rect = None

def reset_ball():
    """Resets the ball to the center and randomizes its starting direction."""
    global ball_speed_x, ball_speed_y
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ball_speed_x = BALL_START_SPEED_X * random.choice((1, -1))
    ball_speed_y = BALL_START_SPEED_Y * random.choice((1, -1))


# MAIN GAME LOOP
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Left Paddle Movement (W/S Keys)
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < SCREEN_HEIGHT:
        left_paddle.y += PADDLE_SPEED

    # Right Paddle Movement (Arrow Keys)
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < SCREEN_HEIGHT:
        right_paddle.y += PADDLE_SPEED

    # 2. GAME LOGIC (Physics & Collisions)

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ceiling and Floor collisions (Bounce vertically)
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1

    # Paddle Collisions using Pygame's colliderect
    if ball.colliderect(left_paddle) and ball_speed_x < 0:
        # Check if ball is moving left to prevent sticky physics glitches
        ball_speed_x *= -1
        # Slightly increase speed on hit for difficulty scaling
        ball_speed_x *= 1.05

    if ball.colliderect(right_paddle) and ball_speed_x > 0:
        # Check if ball is moving right
        ball_speed_x *= -1
        ball_speed_x *= 1.05

    # Scoring Bounds checking (Passing the left/right walls)
    if ball.left <= 0:
        right_score += 1
        reset_ball()

    if ball.right >= SCREEN_WIDTH:
        left_score += 1
        reset_ball()

    #Visuals

    # Clear screen with background color
    screen.fill(COLOR_BG)

    # Draw the middle net line
    pygame.draw.line(screen, COLOR_TEXT, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 2)

    # Draw paddles and ball
    pygame.draw.rect(screen, COLOR_ELEMENTS, left_paddle)
    pygame.draw.rect(screen, COLOR_ELEMENTS, right_paddle)
    pygame.draw.ellipse(screen, COLOR_ELEMENTS, ball) # Draws ball as a circle inside its rectangle

    # Render the scores
    left_text = font.render(str(left_score), True, COLOR_TEXT)
    right_text = font.render(str(right_score), True, COLOR_TEXT)

    # Blit (draw) the text surfaces onto the screen
    screen.blit(left_text, (SCREEN_WIDTH // 4 - left_text.get_width() // 2, 30))
    screen.blit(right_text, (3 * SCREEN_WIDTH // 4 - right_text.get_width() // 2, 30))

    # 67 Easter Egg
    current_time = pygame.time.get_ticks()

        # Check if left score is 6 AND right score is 7
    if left_score == 6 and right_score == 7:
        if not egg_triggered:
                egg_start_time = current_time
                egg_triggered = True
    else:
        # Reset the trigger flag when the score changes so it can happen again if needed
        egg_triggered = False

        # Draw the image if we are within the 1-second (1000ms) window
    if egg_triggered and (current_time - egg_start_time < 1000):
            if egg_image:
                screen.blit(egg_image, egg_rect)


    # Update the full display surface to the screen
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

# Clean quit out of pygame when loop finishes
pygame.quit()
sys.exit()
