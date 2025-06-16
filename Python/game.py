import pygame
import random
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen settings
SCREEN_WIDTH = 350
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
DARK_CYAN = (0, 200, 200)
RED = (255, 0, 0)
DARK_RED = (180, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

# Player settings
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
PLAYER_SPEED = 6

# Bullet settings
BULLET_WIDTH = 6
BULLET_HEIGHT = 12
BULLET_SPEED = 10

# Enemy settings
ENEMY_WIDTH = 35
ENEMY_HEIGHT = 35
ENEMY_SPEED_BASE = 1.5
MAX_ENEMIES = 6
ENEMY_SPAWN_DELAY = 1200  # milliseconds

# Fonts
pygame.font.init()
FONT_SMALL = pygame.font.SysFont("Verdana", 18)
FONT_LARGE = pygame.font.SysFont("Verdana", 36)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooting Game")

# Clock
clock = pygame.time.Clock()

# Load sounds (simple beep for shoot and explosion)
try:
    shoot_sound = pygame.mixer.Sound(
        pygame.mixer.Sound(pygame.mixer.Sound(pygame.mixer.Sound("shoot.wav")))
        if False
        else None
    )
except:
    shoot_sound = None  # No sound loaded
try:
    explosion_sound = (
        pygame.mixer.Sound(pygame.mixer.Sound(pygame.mixer.Sound("explosion.wav")))
        if False
        else None
    )
except:
    explosion_sound = None


# Game objects
class Player:
    def __init__(self):
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = SCREEN_HEIGHT - self.height - 10
        self.speed = PLAYER_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, dx):
        self.x += dx * self.speed
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.rect.x = self.x

    def draw(self, surface):
        # Draw a spaceship shape: a cyan triangle pointing upward with cockpit
        points = [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height),
        ]
        pygame.draw.polygon(surface, CYAN, points)
        # Cockpit
        pygame.draw.polygon(
            surface,
            DARK_CYAN,
            [
                (self.x + self.width // 2, self.y + 8),
                (self.x + 8, self.y + self.height - 8),
                (self.x + self.width - 8, self.y + self.height - 8),
            ],
        )


class Bullet:
    def __init__(self, x, y):
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.x = x
        self.y = y
        self.speed = BULLET_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y

    def draw(self, surface):
        pygame.draw.rect(surface, CYAN, self.rect)


class Enemy:
    def __init__(self):
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = -self.height
        self.speed = ENEMY_SPEED_BASE + random.random() * 1.2
        self.color = RED if random.random() < 0.5 else DARK_RED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self, surface):
        # Draw enemy as a red glowing circle with eyes
        center = (self.x + self.width // 2, self.y + self.height // 2)
        radius = self.width // 2
        # Glow
        glow_surface = pygame.Surface(
            (self.width + 20, self.height + 20), pygame.SRCALPHA
        )
        pygame.draw.circle(
            glow_surface,
            (*self.color, 70),
            (glow_surface.get_width() // 2, glow_surface.get_height() // 2),
            radius + 8,
        )
        surface.blit(glow_surface, (self.x - 10, self.y - 10))
        # Body
        pygame.draw.circle(surface, self.color, center, radius)
        # Eyes
        eye_width = radius // 3
        eye_height = radius // 2
        eye_y = center[1] - radius // 3
        pygame.draw.ellipse(
            surface, BLACK, (center[0] - radius // 2, eye_y, eye_width, eye_height)
        )
        pygame.draw.ellipse(
            surface, BLACK, (center[0] + radius // 6, eye_y, eye_width, eye_height)
        )


def show_text_center(surface, text, font, color, y_offset=0):
    text_surf = font.render(text, True, color)
    rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    surface.blit(text_surf, rect)


def main():
    running = True
    player = Player()
    bullets = []
    enemies = []
    last_enemy_spawn_time = pygame.time.get_ticks()
    score = 0
    lives = 3
    game_over = False

    move_left = False
    move_right = False
    shooting = False
    last_shot_time = 0
    SHOT_COOLDOWN = 350  # milliseconds

    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    move_left = True
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    move_right = True
                if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                    shooting = True
                if event.key == pygame.K_r and game_over:
                    # Restart game
                    main()

            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    move_left = False
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    move_right = False
                if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                    shooting = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # For simplicity: player shoots on any mouse click and moves with arrow keys
                shooting = True
            elif event.type == pygame.MOUSEBUTTONUP:
                shooting = False

        if not game_over:
            # Move player
            dx = 0
            if move_left and not move_right:
                dx = -1
            elif move_right and not move_left:
                dx = 1
            player.move(dx)

            # Shooting
            now = pygame.time.get_ticks()
            if shooting and now - last_shot_time > SHOT_COOLDOWN:
                bullet_x = player.x + player.width // 2 - BULLET_WIDTH // 2
                bullet_y = player.y
                bullets.append(Bullet(bullet_x, bullet_y))
                last_shot_time = now
                if shoot_sound:
                    shoot_sound.play()

            # Update bullets
            for bullet in bullets[:]:
                bullet.update()
                if bullet.y < -bullet.height:
                    bullets.remove(bullet)

            # Spawn enemies
            if (
                now - last_enemy_spawn_time > ENEMY_SPAWN_DELAY
                and len(enemies) < MAX_ENEMIES
            ):
                enemies.append(Enemy())
                last_enemy_spawn_time = now

            # Update enemies
            for enemy in enemies[:]:
                enemy.update()
                if enemy.y > SCREEN_HEIGHT:
                    enemies.remove(enemy)
                    lives -= 1
                    if lives <= 0:
                        game_over = True

            # Check collisions
            for enemy in enemies[:]:
                enemy_rect = enemy.rect
                bullet_hit = False
                for bullet in bullets[:]:
                    if enemy_rect.colliderect(bullet.rect):
                        enemies.remove(enemy)
                        bullets.remove(bullet)
                        score += 10
                        bullet_hit = True
                        if explosion_sound:
                            explosion_sound.play()
                        break
                if bullet_hit:
                    continue

        # Drawing everything
        screen.fill(BLACK)

        # Draw player
        player.draw(screen)

        # Draw bullets
        for bullet in bullets:
            bullet.draw(screen)

        # Draw enemies
        for enemy in enemies:
            enemy.draw(screen)

        # Draw UI - Score and lives
        score_text = FONT_SMALL.render(f"Score: {score}", True, CYAN)
        lives_text = FONT_SMALL.render(f"Lives: {lives}", True, RED)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

        # Draw game over if necessary
        if game_over:
            show_text_center(screen, "GAME OVER", FONT_LARGE, RED, y_offset=-30)
            show_text_center(
                screen, "Press R to Restart", FONT_SMALL, WHITE, y_offset=30
            )

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
