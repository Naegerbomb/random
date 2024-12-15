import os
import pygame
import random
import math

# Initialize pygame
pygame.init()

# Set up game constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CAT_SIZE = 90
DOG_SIZE = 100
MOUSE_SIZE = 20
CHEESE_RADIUS = 70  # Larger cheese
SAFE_ZONE_SIZE = 150
MICE_GOAL = 50
UI_PADDING = 100  # Reserved space in the top-left for UI
CHEESE_SHRINK_RATE = 1  # Pixels per second

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cat vs Dog Game")

# Fonts
font = pygame.font.Font(None, 36)
message_font = pygame.font.Font(None, 72)
endgame_font = pygame.font.Font(None, 150)

# Load assets (use simple rectangles here for simplicity)
cat = pygame.Rect(100, 300, CAT_SIZE, CAT_SIZE)
dog = pygame.Rect(600, 300, DOG_SIZE, DOG_SIZE)
dog2 = None  # Second dog will be added later
cheese = {"x": SCREEN_WIDTH // 2, "y": SCREEN_HEIGHT // 2, "radius": CHEESE_RADIUS}
mice = [pygame.Rect(random.randint(UI_PADDING, SCREEN_WIDTH - MOUSE_SIZE),
                    random.randint(UI_PADDING, SCREEN_HEIGHT - MOUSE_SIZE), 
                    MOUSE_SIZE, MOUSE_SIZE) for _ in range(5)]

# Safe zone (initially hidden)
safe_zone = None

# Game variables
cat_speed = 4.0
dog_speed = 2.8
mice_speed = 0.0
mice_collected = 0
speed_increase = 1.0
dog2_added = False
safe_zone_spawned = False
game_over = False
winner = None  # "dog", "cat", or "mice"

def move_dog(dog):
    if dog.x > cat.x:
        dog.x -= int(dog_speed)
    elif dog.x < cat.x:
        dog.x += int(dog_speed)
    if dog.y > cat.y:
        dog.y -= int(dog_speed)
    elif dog.y < cat.y:
        dog.y += int(dog_speed)

def move_mice():
    for mouse_rect in mice:
        # Calculate avoidance from cat and dogs
        dx_cat = mouse_rect.x - cat.x
        dy_cat = mouse_rect.y - cat.y
        dist_cat = math.hypot(dx_cat, dy_cat)
        
        dx_dog = mouse_rect.x - dog.x
        dy_dog = mouse_rect.y - dog.y
        dist_dog = math.hypot(dx_dog, dy_dog)
        
        dist_dog2 = float('inf')
        if dog2:
            dx_dog2 = mouse_rect.x - dog2.x
            dy_dog2 = mouse_rect.y - dog2.y
            dist_dog2 = math.hypot(dx_dog2, dy_dog2)
        
        # Move toward cheese unless evading
        if dist_cat < 150 or dist_dog < 150 or dist_dog2 < 150:  # Avoid cat/dogs if close
            if dist_cat > 0:
                mouse_rect.x += round((dx_cat / dist_cat) * mice_speed)
                mouse_rect.y += round((dy_cat / dist_cat) * mice_speed)
            if dist_dog > 0:
                mouse_rect.x += round((dx_dog / dist_dog) * mice_speed)
                mouse_rect.y += round((dy_dog / dist_dog) * mice_speed)
            if dog2 and dist_dog2 > 0:
                mouse_rect.x += round((dx_dog2 / dist_dog2) * mice_speed)
                mouse_rect.y += round((dy_dog2 / dist_dog2) * mice_speed)
        else:  # Move toward cheese
            dx_cheese = cheese["x"] - mouse_rect.x
            dy_cheese = cheese["y"] - mouse_rect.y
            dist_cheese = math.hypot(dx_cheese, dy_cheese)
            if dist_cheese > 0:
                mouse_rect.x += round((dx_cheese / dist_cheese) * mice_speed)
                mouse_rect.y += round((dy_cheese / dist_cheese) * mice_speed)

        # Pac-Man-style boundary behavior
        if mouse_rect.x < 0:
            mouse_rect.x = SCREEN_WIDTH
        elif mouse_rect.x > SCREEN_WIDTH:
            mouse_rect.x = 0
        if mouse_rect.y < 0:
            mouse_rect.y = SCREEN_HEIGHT
        elif mouse_rect.y > SCREEN_HEIGHT:
            mouse_rect.y = 0

def draw_ui():
    remaining_text = font.render(f"Mice Remaining: {MICE_GOAL - mice_collected}", True, BLACK)
    screen.blit(remaining_text, (20, 20))

def shrink_cheese():
    global game_over, winner
    for mouse_rect in mice:
        dx = mouse_rect.x - cheese["x"]
        dy = mouse_rect.y - cheese["y"]
        dist = math.hypot(dx, dy)
        if dist <= cheese["radius"]:  # Mouse is "eating" the cheese
            cheese["radius"] -= CHEESE_SHRINK_RATE * (1 / 30)  # Adjust shrink rate for FPS
            if cheese["radius"] <= 0:  # If cheese is fully eaten
                cheese["radius"] = 0
                game_over = True
                winner = "mice"
                break

def add_mice():
    while len(mice) < 5:
        x = random.randint(0, SCREEN_WIDTH - MOUSE_SIZE)
        y = random.randint(UI_PADDING, SCREEN_HEIGHT - MOUSE_SIZE)
        mice.append(pygame.Rect(x, y, MOUSE_SIZE, MOUSE_SIZE))

def end_game_screen():
    screen.fill(WHITE)
    if winner == "dog":
        end_message = endgame_font.render("DOG WINS", True, RED)
    elif winner == "cat":
        end_message = endgame_font.render("CAT WINS", True, GREEN)
    elif winner == "mice":
        end_message = endgame_font.render("MICE WIN", True, BLACK)
    screen.blit(end_message, (SCREEN_WIDTH // 2 - end_message.get_width() // 2, SCREEN_HEIGHT // 2 - end_message.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    if game_over:
        end_game_screen()
        running = False
        break

    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Cat movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and cat.x - cat_speed >= 0:
        cat.x -= int(cat_speed)
    if keys[pygame.K_RIGHT] and cat.x + cat_speed <= SCREEN_WIDTH - CAT_SIZE:
        cat.x += int(cat_speed)
    if keys[pygame.K_UP] and cat.y - cat_speed >= 0:
        cat.y -= int(cat_speed)
    if keys[pygame.K_DOWN] and cat.y + cat_speed <= SCREEN_HEIGHT - CAT_SIZE:
        cat.y += int(cat_speed)

    # Dog movement
    move_dog(dog)

    # Add second dog after 40 mice are eaten
    if mice_collected >= 40 and not dog2_added:
        dog2 = pygame.Rect(400, 600, DOG_SIZE, DOG_SIZE)
        dog2_added = True

    # Move the second dog if added
    if dog2:
        move_dog(dog2)

    # Mice movement
    move_mice()

    # Shrink the cheese
    shrink_cheese()

    # Check collisions with mice
    for mouse_rect in mice[:]:
        if cat.colliderect(mouse_rect):
            mice.remove(mouse_rect)
            mice_collected += 1
            cat_speed += speed_increase  # Increase cat speed
            if mice_collected >= 10:
                mice_speed = 1.0 + (mice_collected - 10) * 0.1  # Gradual speed increase

    # Spawn safe zone randomly after goal is reached
    if mice_collected >= MICE_GOAL and not safe_zone_spawned:
        safe_zone = pygame.Rect(
            random.randint(0, SCREEN_WIDTH - SAFE_ZONE_SIZE),
            random.randint(0, SCREEN_HEIGHT - SAFE_ZONE_SIZE),
            SAFE_ZONE_SIZE,
            SAFE_ZONE_SIZE,
        )
        safe_zone_spawned = True

    # Check if cat and dog collide
    if cat.colliderect(dog) or (dog2 and cat.colliderect(dog2)):
        game_over = True
        winner = "dog"

    # Check if the cat wins by reaching the safe zone
    if safe_zone_spawned and cat.colliderect(safe_zone):
        game_over = True
        winner = "cat"

    # Add new mice
    add_mice()

    # Draw cheese
    pygame.draw.circle(screen, YELLOW, (cheese["x"], cheese["y"]), int(cheese["radius"]))

    # Draw safe zone if spawned
    if safe_zone:
        pygame.draw.rect(screen, BLUE, safe_zone)

    # Draw cat, dogs, and mice
    pygame.draw.rect(screen, GREEN, cat)
    pygame.draw.rect(screen, RED, dog)
    if dog2:
        pygame.draw.rect(screen, RED, dog2)
    for mouse_rect in mice:
        pygame.draw.rect(screen, BLACK, mouse_rect)

    # Draw UI
    draw_ui()

    # Update the screen
    pygame.display.flip()
    clock.tick(30)

# Quit pygame
pygame.quit()

