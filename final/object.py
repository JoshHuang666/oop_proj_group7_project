import pygame

class GameObject:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

class RegularPlayer(GameObject):
    def __init__(self, x, y, size, color):
        super().__init__(x, y, size, size, color)
        self.vel = 0

    def jump(self):
        self.vel = -10
        jump_sound = pygame.mixer.Sound('final/audio/jump1.wav')
        jump_sound.play()

class HeavyPlayer(RegularPlayer):
    def __init__(self, x, y, size, color):
        super().__init__(x, y, size, color)

    def jump(self):
        self.vel = -5
        jump_sound = pygame.mixer.Sound('final/audio/jump3.wav')
        jump_sound.play()

class SmallPlayer(RegularPlayer):
    def __init__(self, x, y, size, color):
        super().__init__(x, y, size, color)
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