import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up display
WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Cube")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
BLUE = (0, 0, 255)

# Load Sound files
jump_sound = pygame.mixer.Sound('final/audio/jump1.wav')
jump_sound.set_volume(1.0) # Set the volume to 100% 
score_sound = pygame.mixer.Sound('final/audio/score.wav')
game_over_sound = pygame.mixer.Sound('final/audio/game_over.wav')
game_over_sound.set_volume(1.0) # Set the volume to 100%

pygame.time.delay(1000)
background_music = pygame.mixer.music.load('final/audio/background.wav')
pygame.mixer.music.set_volume(0.5)

# Score
font = pygame.font.SysFont(None, 30)

# Background image
background_image = pygame.image.load('final/images/background.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

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

class GameObject:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

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

class Game:
    BUTTON_GAP = 20

    def __init__(self):
        self.players = [RegularPlayer, HeavyPlayer, SmallPlayer]  # List of player classes
        self.player_parameters = [(50, HEIGHT // 2 - 25, 50, WHITE), (50, HEIGHT // 2 - 25, 50, BLUE), (50, HEIGHT // 2 - 25, 30, BLACK)]  # List of player classes
        self.current_player_index = 0  # Start with the first player class
        self.player = self.get_current_player()  # Get the current player object
        self.obstacles = []
        self.score = 0
        self.best_scores = [0]  # List to store all scores obtained from previous games

        # Create buttons
        self.create_buttons()

        self.game_started = False
        self.game_over = False

        # Create left button
        left_button_width, left_button_height = 50, 50
        left_button_x = WIDTH // 2 - 100
        left_button_y = HEIGHT // 2
        self.left_button = LeftButton(left_button_x, left_button_y, left_button_width, left_button_height, None, None)

        # Create right button
        right_button_width, right_button_height = 50, 50
        right_button_x = WIDTH // 2 + 50
        right_button_y = HEIGHT // 2
        self.right_button = RightButton(right_button_x, right_button_y, right_button_width, right_button_height, None, None)

        # Create current player image
        self.current_player_image = pygame.Surface((50, 50))
        self.current_player_image_rect = self.current_player_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        # Create pause button
        pause_button_x = WIDTH - 50
        pause_button_y = 0
        self.pause_button = PauseButton(pause_button_x, pause_button_y, 50, 50, pause_button_image)

        # Create resume button
        resume_button_width, resume_button_height = 150, 50
        resume_button_x = (WIDTH - resume_button_width) // 2
        resume_button_y = HEIGHT // 2 + 50
        self.resume_button = Button(resume_button_x, resume_button_y, resume_button_width, resume_button_height, GRAY, 'Resume')

        # Create restart button
        restart_button_width, restart_button_height = 150, 50
        restart_button_x = (WIDTH - restart_button_width) // 2
        restart_button_y = HEIGHT // 2 + 120
        self.restart_button = Button(restart_button_x, restart_button_y, restart_button_width, restart_button_height, GRAY, 'Restart')

        self.paused = False

    def create_buttons(self):
        # Start button
        button_width, button_height = 100, 50
        button_x = (WIDTH - button_width) // 2
        start_button_y = HEIGHT // 2 - button_height - self.BUTTON_GAP // 2
        self.start_button = Button(button_x, start_button_y, button_width, button_height, GRAY, 'Start')

        # Ranking button
        ranking_button_y = start_button_y + self.BUTTON_GAP * 8  # Adjusted gap
        self.ranking_button = Button(button_x, ranking_button_y, button_width, button_height, GRAY, 'Ranking')

        # Select button
        select_button_y = start_button_y + self.BUTTON_GAP * 4  # Adjusted gap
        self.select_button = Button(button_x, select_button_y, button_width, button_height, GRAY, 'Select')

        #Setting button
        setting_button_x = WIDTH - 50  # Adjusted x-coordinate
        setting_button_y = 0  # Adjusted y-coordinate
        self.setting_button = SettingButton(setting_button_x, setting_button_y, button_width, button_height, setting_button_image)

    def generate_obstacle(self):
        gap = 150
        obstacle_width = 40
        top_height = random.randint(50, HEIGHT - gap - 50)
        bottom_height = HEIGHT - top_height - gap
        
        # Define the probabilities for each color
        color_probabilities = [(GREEN, 6), (RED, 3), (GOLD, 1)]
        
        # Choose a random color based on the probabilities
        color_choices = [color for color, prob in color_probabilities for _ in range(prob)]
        color = random.choice(color_choices)
        
        top_obstacle = Obstacle(WIDTH, 0, obstacle_width, top_height, color)
        bottom_obstacle = Obstacle(WIDTH, top_height + gap, obstacle_width, bottom_height, color)
        self.obstacles.extend([top_obstacle, bottom_obstacle])

    def draw_score(self):
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        WIN.blit(score_text, (10, 10))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.game_started and not self.game_over:
                    if self.start_button.is_clicked(pygame.mouse.get_pos()):
                        self.start_game()
                    elif self.ranking_button.is_clicked(pygame.mouse.get_pos()):
                        self.show_ranking()
                    elif self.select_button.is_clicked(pygame.mouse.get_pos()):
                        self.show_character_select_window()  # Show character select window when select button is clicked
                    elif self.setting_button.is_clicked(pygame.mouse.get_pos()):
                        self.show_setting_window()
                elif self.game_over:
                    if self.start_button.is_clicked(pygame.mouse.get_pos()):
                        self.start_game()  # Restart the game when start button is clicked
                    elif self.ranking_button.is_clicked(pygame.mouse.get_pos()):
                        self.show_ranking()  # Show ranking when ranking button is clicked
                    elif self.select_button.is_clicked(pygame.mouse.get_pos()):
                        self.show_character_select_window()  # Show character select window when select button is clicked
                    elif self.setting_button.is_clicked(pygame.mouse.get_pos()):
                        self.show_setting_window() #Show setting window when setting button is clicked
                elif self.paused:
                    if self.resume_button.is_clicked(pygame.mouse.get_pos()):
                        self.paused = False
                    elif self.restart_button.is_clicked(pygame.mouse.get_pos()):
                        self.start_game()
                        self.paused = False
                else:
                    if self.pause_button.is_clicked(pygame.mouse.get_pos()):
                        self.paused = True
            if event.type == pygame.KEYDOWN and self.game_started and not self.paused:  # Only handle key events when the game is started
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
        return True

    def start_game(self):
        self.game_started = True
        self.score = 0
        self.player.rect.y = HEIGHT // 2 - 25
        self.player.vel = 0  # Reset player's velocity
        self.obstacles = []
        self.game_over = False
        pygame.mixer.music.stop()
        background_music = pygame.mixer.music.load('audio/background.wav')  # Load the new background music
        pygame.mixer.music.play(-1)  # Play the new background music indefinitely

    def update(self):
        if self.game_started and not self.paused:  # Update the game only if it's not paused
            self.player.rect.y += self.player.vel
            self.player.vel += 1

            if self.player.rect.y <= 0 or self.player.rect.y + self.player.rect.height >= HEIGHT:
                self.end_game()

            if len(self.obstacles) == 0 or self.obstacles[-1].rect.x < WIDTH - 200:
                self.generate_obstacle()

            for obstacle in self.obstacles:
                obstacle.rect.x -= 5
                if obstacle.rect.colliderect(self.player.rect):
                    self.end_game()
                else:
                    if not obstacle.collided and obstacle.rect.x + obstacle.rect.width < self.player.rect.x:
                        obstacle.collided = True
                        if obstacle.color == GREEN:
                            self.score += 1
                        elif obstacle.color == RED:
                            self.score += 3
                        elif obstacle.color == GOLD:
                            self.score += 5
            self.obstacles = [obstacle for obstacle in self.obstacles if obstacle.rect.x + obstacle.rect.width > 0]
        return True

    def draw(self):
        if not self.paused:  # Only draw game elements if the game is not paused
            WIN.blit(background_image, (0, 0))
            self.player.draw(WIN)
            for obstacle in self.obstacles:
                obstacle.draw(WIN)
            self.draw_score()
            if not self.game_started:
                if not self.game_over:
                    self.start_button.draw(WIN, WHITE)
                    self.select_button.draw(WIN, WHITE)
                    self.ranking_button.draw(WIN, WHITE)
                    self.setting_button.draw(WIN)
                else:
                    self.start_button.draw(WIN, WHITE)
                    self.select_button.draw(WIN, WHITE)
                    self.ranking_button.draw(WIN, WHITE)
                    self.setting_button.draw(WIN)
            elif self.game_started and not self.game_over:
                self.pause_button.draw(WIN)
            pygame.display.update()
        else:
            # Draw pause text
            font = pygame.font.SysFont('comicsans', 50)
            text = font.render('Paused', 1, WHITE)
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

            # Draw resume button
            self.resume_button.draw(WIN)

            #Draw restart button
            self.restart_button.draw(WIN)

            pygame.display.update()

    def end_game(self):
        self.game_started = False
        self.game_over = True
        self.best_scores.append(self.score)  # Add the current score to the list of all scores
        self.best_scores.sort(reverse=True)  # Sort the list of all scores in descending order
        self.best_scores = self.best_scores[:3]  # Update the best three scores
        self.player.vel = 0  # Reset the player's velocity for the next game
        self.paused = False  # Ensure game is not paused when ending
        pygame.mixer.music.stop()
        game_over_sound.play() 
        background_music = pygame.mixer.music.load('audio/background_music2.wav')  # Load the new background music
        pygame.mixer.music.play(-1)  # Play the new background music indefinitely

    def show_ranking(self):
        ranking = self.best_scores  # Get the best three scores
        while len(ranking) < 3:  # Fill the remaining slots with zeros if needed
            ranking.append(0)
        ranking_screen = True
        return_button_x = (WIDTH - 50) // 2
        return_button_y = HEIGHT - 100
        return_button_rect = pygame.Rect(return_button_x, return_button_y, 50, 50)
        while ranking_screen:
            WIN.blit(background_image, (0, 0))
            font = pygame.font.SysFont('comicsans', 40)
            title = font.render('Best Scores', 1, WHITE)
            WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
            for i, score in enumerate(ranking):
                text = font.render(str(score), 1, WHITE)
                WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, 150 + i * 50))

            # Draw return button
            WIN.blit(return_button_image, (return_button_x, return_button_y))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ranking_screen = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if return_button_rect.collidepoint(event.pos):  # Check if return button is clicked
                        ranking_screen = False

    def show_character_select_window(self):
       # Character select window
        character_select_window = True
        return_button_x = (WIDTH - 50) // 2
        return_button_y = HEIGHT - 100
        return_button_rect = pygame.Rect(return_button_x, return_button_y, 50, 50)

        while character_select_window:
            WIN.blit(background_image, (0, 0))  # Draw background image

            # Draw current player's image
            self.update_current_player_image()

            # Draw text describing player characteristics
            font = pygame.font.SysFont('comicsans', 24)
            text = font.render(self.get_current_player_description(), 1, BLACK)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
            
            # Create a surface with a white background
            description_surface = pygame.Surface((text_rect.width + 10, text_rect.height + 10))
            description_surface.fill(WHITE)

            # Blit the text onto the description surface
            description_surface.blit(text, (5, 5))

            # Blit the description surface onto the window
            WIN.blit(description_surface, (text_rect.x - 5, text_rect.y - 5))


            self.left_button.draw(WIN)
            self.right_button.draw(WIN)

            # Draw return button
            WIN.blit(return_button_image, (return_button_x, return_button_y))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if left button is clicked
                    if self.left_button.rect.collidepoint(event.pos):
                        # Switch to the previous character
                        self.player = self.switch_to_previous_character()
                        # Redraw the current player's image
                        self.update_current_player_image()
                    # Check if right button is clicked
                    elif self.right_button.rect.collidepoint(event.pos):
                        # Switch to the next character
                        self.player = self.switch_to_next_character()
                        # Redraw the current player's image
                        self.update_current_player_image()
                    # Check if return button is clicked
                    elif return_button_rect.collidepoint(event.pos):
                        character_select_window = False

    def show_setting_window(self):
        setting_window = True
        return_button_x = (WIDTH - 50) // 2
        return_button_y = HEIGHT - 100
        return_button_rect = pygame.Rect(return_button_x, return_button_y, 50, 50)

        while setting_window:
            WIN.blit(background_image, (0, 0))
            # Display setting window content
            self.display_setting_window(WIN)

            # Draw return button
            WIN.blit(return_button_image, (return_button_x, return_button_y))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    setting_window = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if return button is clicked
                    if return_button_rect.collidepoint(event.pos):
                        setting_window = False

    def display_setting_window(self, window):
        font = pygame.font.SysFont('comicsans', 36)
        text = [
            "Game Rules:",
            "- Press SPACE to make the cube jump.",
            "- Avoid colliding with obstacles.",
            "- Collect green obstacles to score 1 point.",
            "- Collect red obstacles to score 3 points.",
            "- Collect gold obstacles to score 5 points.",
            "- Have fun!"
        ]
        y_offset = 50
        for line in text:
            line_surface = font.render(line, True, BLACK)  # Render text with black color
            line_rect = line_surface.get_rect(center=(WIDTH // 2, y_offset))
        
            # Create a surface with a white background
            background_surface = pygame.Surface((line_rect.width + 20, line_rect.height + 20))
            background_surface.fill(WHITE)
        
            # Blit the text onto the background surface
            background_surface.blit(line_surface, (10, 10))
        
            # Blit the background surface onto the window
            window.blit(background_surface, (line_rect.x - 10, line_rect.y - 10))
        
            y_offset += 40  # Adjust vertical spacing

    def switch_to_previous_character(self):
        self.current_player_index -= 1
        if self.current_player_index < 0:
            self.current_player_index = len(self.players) - 1
        return self.get_current_player()

    def switch_to_next_character(self):
        self.current_player_index += 1
        if self.current_player_index >= len(self.players):
            self.current_player_index = 0
        return self.get_current_player()

    def get_current_player(self):
        player_class = self.players[self.current_player_index]
        player_params = self.player_parameters[self.current_player_index]
        return player_class(*player_params)  # Instantiate player object with parameters
    
    def update_current_player_image(self):
        if self.current_player_index == 0 or self.current_player_index == 1:
            self.current_player_image = pygame.Surface((50, 50))
            self.current_player_image_rect = self.current_player_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            if self.current_player_index == 0:
                self.current_player_image.fill(WHITE)
            elif self.current_player_index == 1:
                self.current_player_image.fill(BLUE)
        elif self.current_player_index == 2:
            self.current_player_image = pygame.Surface((30, 30))
            self.current_player_image.fill(BLACK)
            self.current_player_image_rect = self.current_player_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 5))

        # Draw the current player's image onto the surface
        self.player.draw(self.current_player_image)

        # Blit the updated image onto the window
        WIN.blit(self.current_player_image, self.current_player_image_rect)

    def get_current_player_description(self):
        descriptions = ["Regular Player: Jumps normally.",
                        "Heavy Player: Jumps less higher.",
                        "Small Player: Smaller size."]
        return descriptions[self.current_player_index]
        
    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(30)
            running = self.handle_events()
            if not running:
                break

            running = self.update()
            if not running:
                break

            self.draw()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
