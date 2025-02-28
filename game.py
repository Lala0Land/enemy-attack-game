import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen parameters
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Click the Enemies")

clock = pygame.time.Clock()

# Center of the screen and its circle
CENTER = (WIDTH // 2, HEIGHT // 2)
CENTER_RADIUS = 50

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

class Enemy:
    def __init__(self):
        # Randomly choose a side for the enemy to appear from
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            self.x = 0
            self.y = random.randint(0, HEIGHT)
        elif side == "right":
            self.x = WIDTH
            self.y = random.randint(0, HEIGHT)
        elif side == "top":
            self.x = random.randint(0, WIDTH)
            self.y = 0
        elif side == "bottom":
            self.x = random.randint(0, WIDTH)
            self.y = HEIGHT

        self.radius = 20  # Enemy size
        self.speed = 3  # Enemy speed

        # Calculate movement direction
        dx = CENTER[0] - self.x
        dy = CENTER[1] - self.y
        distance = math.hypot(dx, dy)
        self.vx = (dx / distance) * self.speed
        self.vy = (dy / distance) * self.speed

    def update(self):
        # Move enemy towards the center
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (int(self.x), int(self.y)), self.radius)

    def is_clicked(self, pos):
        mx, my = pos
        return math.hypot(self.x - mx, self.y - my) <= self.radius

    def collides_with_center(self):
        dx = self.x - CENTER[0]
        dy = self.y - CENTER[1]
        distance = math.hypot(dx, dy)
        return distance <= (CENTER_RADIUS + self.radius)

def main():
    running = True
    enemies = []
    score = 0
    font = pygame.font.SysFont(None, 36)

    SPAWN_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_ENEMY, 1000)

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPAWN_ENEMY:
                enemies.append(Enemy())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for enemy in enemies[:]:
                    if enemy.is_clicked(pos):
                        enemies.remove(enemy)
                        score += 1
                        break

        for enemy in enemies:
            enemy.update()
            if enemy.collides_with_center():
                running = False

        screen.fill(BLACK)
        pygame.draw.circle(screen, BLUE, CENTER, CENTER_RADIUS)
        for enemy in enemies:
            enemy.draw(screen)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()


