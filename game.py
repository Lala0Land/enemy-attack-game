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
RED1 = (255, 0, 0)
RED2 = (178,34,34)
RED3 = (220,20,60)
RED4 = (205,92,92)
RED5 = (139,0,0)
RED6 = (255,99,71)
RED7 = (255,69,0)
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

        self.radius = random.choice((15, 17, 20, 23))    # Enemy radius
        self.speed = random.choice((1, 2, 3, 4))  # Enemy speed

        # Calculate the direction vector from enemy to the center
        dx = CENTER[0] - self.x
        dy = CENTER[1] - self.y
        distance = math.hypot(dx, dy)  # Distance to center
        self.vx = (dx / distance) * self.speed
        self.vy = (dy / distance) * self.speed

    def update(self):
        # Update the enemy's position
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        # Draw the enemy
        pygame.draw.circle(surface, RED1, (int(self.x),
                                                                                              int(self.y)), self.radius)

    def is_clicked(self, pos):
        # Check if the enemy was clicked
        mx, my = pos
        return math.hypot(self.x - mx, self.y - my) <= self.radius

    def collides_with_center(self):
        # Check if the enemy has collided with the center
        dx = self.x - CENTER[0]
        dy = self.y - CENTER[1]
        distance = math.hypot(dx, dy)
        return distance <= (CENTER_RADIUS + self.radius)

class Particle:
    def __init__(self, x, y, color=RED1):
        self.x = x
        self.y = y
        self.life = random.randint(20, 40)  # Particle lifespan (frames)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.size = random.randint(2, 4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

def main():
    running = True
    enemies = []    # List of enemies
    particles = []  # List of particles for explosion animation
    score = 0       # Player score
    font = pygame.font.SysFont(None, 36)

    # Event for spawning enemies every second
    SPAWN_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_ENEMY, 900)

    while running:
        clock.tick(60)  # 60 FPS limit

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPAWN_ENEMY:
                enemies.append(Enemy())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Check if an enemy was clicked
                for enemy in enemies[:]:
                    if enemy.is_clicked(pos):
                        # Create explosion effect (particles)
                        for _ in range(20):
                            particles.append(Particle(enemy.x, enemy.y))
                        enemies.remove(enemy)
                        score += 1
                        break

        # Update enemies
        for enemy in enemies:
            enemy.update()
            # If an enemy reaches the center, the game ends
            if enemy.collides_with_center():
                running = False

        # Update particles
        for particle in particles[:]:
            particle.update()
            if particle.life <= 0:
                particles.remove(particle)

        # Draw everything
        screen.fill(BLACK)
        pygame.draw.circle(screen, BLUE, CENTER, CENTER_RADIUS)
        for enemy in enemies:
            enemy.draw(screen)
        for particle in particles:
            particle.draw(screen)
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    # Game over screen
    screen.fill(BLACK)
    game_over_text = font.render("Game Over. Score: " + str(score), True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()

if __name__ == "__main__":
    main()

