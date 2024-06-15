import pygame

WHITE = (255, 255, 255)

# Return button image
return_button_image = pygame.image.load('final/images/return.png')
return_button_image = pygame.transform.scale(return_button_image, (50, 50)) 

# Left button image
left_button_image = pygame.image.load('final/images/left.png').convert_alpha()
left_button_image = pygame.transform.scale(left_button_image, (50, 50))

# Right button image
right_button_image = pygame.image.load('final/images/right.png').convert_alpha()
right_button_image = pygame.transform.scale(right_button_image, (50, 50))

# Setting button image
setting_button_image = pygame.image.load('final/images/setting.png').convert_alpha()
setting_button_image = pygame.transform.scale(setting_button_image, (50, 50))

# Pause button image
pause_button_image = pygame.image.load('final/images/pause.png').convert_alpha()
pause_button_image = pygame.transform.scale(pause_button_image, (50, 50))

# Sound button image
louder_button_image = pygame.image.load('final/images/loudersound.png').convert_alpha()
louder_button_image = pygame.transform.scale(louder_button_image, (50, 50))
lower_button_image = pygame.image.load('final/images/lowersound.png').convert_alpha()
lower_button_image = pygame.transform.scale(lower_button_image, (50, 50))
mute_button_image = pygame.image.load('final/images/mute.png').convert_alpha()
mute_button_image = pygame.transform.scale(mute_button_image, (50, 50))

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
    
class LeftButton(Button):
    def __init__(self, x, y, width, height, color, text):
        super().__init__(x, y, width, height, color, text)

    def draw(self, window):
        window.blit(left_button_image, (self.rect.x, self.rect.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class RightButton(Button):
    def __init__(self, x, y, width, height, color, text):
        super().__init__(x, y, width, height, color, text)

    def draw(self, window):
        window.blit(right_button_image, (self.rect.x, self.rect.y))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class SettingButton(Button):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, None)
        self.image = image

    def draw(self, window):
        window.blit(setting_button_image, (self.rect.x, self.rect.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
class PauseButton(Button):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, None)
        self.image = image

    def draw(self, window):
        window.blit(pause_button_image, (self.rect.x, self.rect.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
class SoundButton(Button):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, None)
        self.image = image

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def handle_event(self, event, volume):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False