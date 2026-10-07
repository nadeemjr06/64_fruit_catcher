import pygame
from game.basket import Basket
from game.fruit import Fruit
import random
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y

        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-4, -1)

        self.gravity = 0.15

        self.lifetime = random.randint(20, 35)
        self.size = random.randint(2, 5)

        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy

        self.vy += self.gravity

        self.lifetime -= 1

    def draw(self, surface):
        pygame.draw.circle(
            surface,
            self.color,
            (int(self.x), int(self.y)),
            self.size
        )

    def is_dead(self):
        return self.lifetime <= 0
class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.basket = Basket(width, height)
        self.fruits = []
        self.particles = []
        self.score = 0
        self.lives = 3
        self.spawn_delay = 750
        self.last_spawn_time = pygame.time.get_ticks()
        # Dynamic difficulty settings
        self.base_fall_speed = 4.0
        self.speed_increment = 0.15

        self.base_spawn_delay = 1000
        self.spawn_delay_reduction = 25
        self.min_spawn_delay = 300
        self.game_state = "PLAYING"

        self.font_big = pygame.font.SysFont(None, 48)
        self.font_medium = pygame.font.SysFont(None, 28)

    def handle_event(self, event):
        if self.game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()
    def create_splash(self, x, y, color):
        for _ in range(12):
            self.particles.append(
                Particle(x, y, color)
            )
    def update(self):
        if self.game_state != "PLAYING":
            return
        self.update_difficulty()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.basket.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.basket.move_right()

        now = pygame.time.get_ticks()
        if now - self.last_spawn_time >= self.spawn_delay:
            spawn_roll = random.random()

            if spawn_roll < 0.10:
                fruit_type = "bomb"

            elif spawn_roll < 0.25:
                fruit_type = "rotten"

            else:
                fruit_type = "normal"

            self.fruits.append(
                Fruit(self.width, fruit_type,self.current_fall_speed)
            )

            self.last_spawn_time = now

        basket_rect = self.basket.rect
        for fruit in self.fruits[:]:
            fruit.update()

            if basket_rect.colliderect(fruit.rect):

                if fruit.fruit_type == "normal":

                    # Normal fruit → reward
                    self.score += 1
                    self.create_splash(fruit.x,fruit.y,fruit.color)

                elif fruit.fruit_type == "rotten":

                    # Rotten fruit → lose 1 point
                    self.score = max(0, self.score - 1)
                    self.create_splash(fruit.x,fruit.y,fruit.color)

                elif fruit.fruit_type == "bomb":

                    # Bomb → lose 1 life
                    self.lives -= 1
                    self.create_splash(fruit.x,fruit.y,fruit.color)

                self.fruits.remove(fruit)

                # Check whether the player has lost all lives
                if self.lives <= 0:
                    self.game_state = "You lost bro"

                continue
            if fruit.is_missed(self.height):
                self.create_splash(fruit.x,fruit.y,fruit.color)
            # Missing any falling object costs one life
                if fruit.fruit_type =="normal":
                    self.lives -= 1

                    # Check Game Over
                    if self.lives <= 0:
                        self.game_state = "GAME_OVER"
                self.fruits.remove(fruit)
        for particle in self.particles[:]:

            particle.update()

            if particle.is_dead():
                self.particles.remove(particle)    

    def reset(self):
        self.basket = Basket(self.width, self.height)
        self.fruits.clear()
        self.score = 0
        self.lives = 3
        self.last_spawn_time = pygame.time.get_ticks()
        self.game_state = "PLAYING"

    def render(self, screen):
        screen.fill((28, 32, 40))

        ground_y = self.height - 25
        pygame.draw.rect(screen, (45, 50, 60), (0, ground_y, self.width, 25))

        self.basket.render(screen)
        for fruit in self.fruits:
            fruit.render(screen)
        for particle in self.particles:
            particle.draw(screen)

        score_surf = self.font_medium.render(f"Score: {self.score}", True, (255, 220, 80))
        screen.blit(score_surf, (25, 20))

        lives_surf = self.font_medium.render(f"Lives: {self.lives}", True, (240, 80, 80))
        screen.blit(lives_surf, (self.width - lives_surf.get_width() - 25, 20))

        if self.game_state == "GAME_OVER":
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))

            over_surf = self.font_big.render("You lost bro", True, (235, 70, 70))
            screen.blit(over_surf, (self.width // 2 - over_surf.get_width() // 2, self.height // 2 - 40))

            final_surf = self.font_medium.render(f"Final Score: {self.score}", True, (255, 255, 255))
            screen.blit(final_surf, (self.width // 2 - final_surf.get_width() // 2, self.height // 2 + 10))

            restart_surf = self.font_medium.render("Press [R] to Play Again", True, (200, 200, 200))
            screen.blit(restart_surf, (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 50))

    def update_difficulty(self):
        # Increase falling speed as score increases
        self.current_fall_speed = (
        self.base_fall_speed +
        self.score * self.speed_increment
        )

        # Decrease spawn delay as score increases
        self.spawn_delay = max(
        self.min_spawn_delay,
        self.base_spawn_delay -
        self.score * self.spawn_delay_reduction
        )
