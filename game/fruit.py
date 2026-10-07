import random
import pygame


class Fruit:
    def __init__(self, screen_width, fruit_type="normal", speed=4.0):
        self.screen_width = screen_width

        self.radius = 14
        self.x = random.randint(30, screen_width - 30)
        self.y = -self.radius * 2

        self.speed = speed

        self.fruit_type = fruit_type

        if fruit_type == "rotten":
            self.color = (100, 180, 50)      # Green rotten fruit

        elif fruit_type == "bomb":
            self.color = (30, 30, 30)        # Black bomb

        else:
            self.color = random.choice([
                (230, 45, 45),    # Apple
                (245, 140, 30),   # Orange
                (160, 60, 200),   # Grape
            ])

    def update(self):
        self.y += self.speed

    def is_missed(self, screen_height):
        return self.y > screen_height

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )

    def render(self, surface):
        center = (int(self.x), int(self.y))

        pygame.draw.circle(
            surface,
            self.color,
            center,
            self.radius
        )

        # Normal fruit highlight
        if self.fruit_type == "normal":
            pygame.draw.circle(
                surface,
                (255, 255, 255),
                (int(self.x - 4), int(self.y - 4)),
                3
            )

        # Rotten fruit marking
        elif self.fruit_type == "rotten":
            pygame.draw.circle(
                surface,
                (60, 60, 30),
                (int(self.x + 4), int(self.y - 3)),
                4
            )

        # Bomb fuse
        elif self.fruit_type == "bomb":
            pygame.draw.line(
                surface,
                (200, 150, 50),
                (int(self.x), int(self.y - self.radius)),
                (int(self.x + 5), int(self.y - self.radius - 6)),
                2
            )