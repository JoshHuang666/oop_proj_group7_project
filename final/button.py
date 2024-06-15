import pygame

WHITE = (255, 255, 255)

class Button:
    def __init__(self, x, y, width, height, color, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.SysFont(None, 30)

    def draw(self, window, outline=None):
        if outline:
            pygame.draw.rect(window, outline, self.rect, 0)
        
        pygame.draw.rect(window, self.color, self.rect, 0)

        if self.text != '':
            text = self.font.render(self.text, 1, WHITE)
            window.blit(text, (self.rect.x + (self.rect.width / 2 - text.get_width() / 2), self.rect.y + (self.rect.height / 2 - text.get_height() / 2)))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
class ImagesButton(Button):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, None)
        self.image = image

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False