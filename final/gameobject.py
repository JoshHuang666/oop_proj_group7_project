import pygame
import random

GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

class GameObject:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

class RegularPlayer(GameObject):
    def __init__(self, x, y, size, image):
        super().__init__(x, y, size, size, image)
        self.image = pygame.transform.scale(image, (size, size))
        self.vel = 0

    def draw(self, window):
        window.blit(self.image, self.rect.topleft)

    def jump(self):
        self.vel = -10
        jump_sound = pygame.mixer.Sound('final/audio/jump1.wav')
        jump_sound.play()

class HeavyPlayer(RegularPlayer):
    def __init__(self, x, y, size, image):
        super().__init__(x, y, size, image)

    def jump(self):
        self.vel = -5
        jump_sound = pygame.mixer.Sound('final/audio/jump3.wav')
        jump_sound.play()

class SmallPlayer(RegularPlayer):
    def __init__(self, x, y, size, image):
        super().__init__(x, y, size, image)
        self.size = size // 2

    def jump(self):
        self.vel = -13
        jump_sound = pygame.mixer.Sound('final/audio/jump2.wav')
        jump_sound.play()

class Obstacle(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.collided = False
        self.color = color

    def generate_obstacle(window_width, obstacles_list, gap):
        obstacle_width = 40
        top_height = random.randint(50, window_width - gap - 50)
        bottom_height = window_width - top_height - gap

        # Define the probabilities for each color
        color_probabilities = [(GREEN, 6), (RED, 3), (GOLD, 1)]

        # Choose a random color based on the probabilities
        color_choices = [color for color, prob in color_probabilities for _ in range(prob)]
        color = random.choice(color_choices)

        top_obstacle = Obstacle(window_width, 0, obstacle_width, top_height, color)
        bottom_obstacle = Obstacle(window_width, top_height + gap, obstacle_width, bottom_height, color)
        obstacles_list.extend([top_obstacle, bottom_obstacle])
