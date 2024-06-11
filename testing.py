import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)

# Score
font = pygame.font.SysFont(None, 30)

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
        if pos[0] > self.rect.x and pos[0] < self.rect.x + self.rect.width:
            if pos[1] > self.rect.y and pos[1] < self.rect.y + self.rect.height:
                return True
        return False

class Player(GameObject):
    def __init__(self, x, y, size, color):
        super().__init__(x, y, size, size, color)
        self.vel = 0

    def jump(self):
        self.vel = -10

class Obstacle(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
        self.collided = False

class Game:
    button_gap = 20

    def __init__(self):
        self.player = Player(50, HEIGHT // 2 - 25, 50, WHITE)
        self.obstacles = []
        self.score = 0
        self.best_scores = [0]  # List to store all scores obtained from previous games

        # Adjust button sizes for smaller window
        button_width, button_height = 100, 50
        button_x = (WIDTH - button_width) // 2
        self.start_button = Button(button_x, HEIGHT // 2 - button_height - self.button_gap // 2, button_width, button_height, GRAY, 'Start')
        self.record_button = None
        self.ranking_button = Button(button_x, HEIGHT // 2 + self.button_gap * 2, button_width, button_height, GRAY, 'Ranking')

        self.game_started = False
        self.game_over = False

    def generate_obstacle(self):
        gap = 150
        obstacle_width = 40
        top_height = random.randint(50, HEIGHT - gap - 50)
        bottom_height = HEIGHT - top_height - gap
        top_obstacle = Obstacle(WIDTH, 0, obstacle_width, top_height, WHITE)
        bottom_obstacle = Obstacle(WIDTH, top_height + gap, obstacle_width, bottom_height, WHITE)
        self.obstacles.extend([top_obstacle, bottom_obstacle])

    def draw_score(self):
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        WIN.blit(score_text, (10, 10))

    def draw_best_scores(self):
        for i, score in enumerate(self.best_scores):
            score_text = font.render(f"{i+1}: {score}", True, WHITE)
            WIN.blit(score_text, (WIDTH - 100, 10 + 30 * i))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.game_started and not self.game_over:
                    if self.start_button.is_clicked(pygame.mouse.get_pos()):
                        self.start_game()
                elif self.game_over:
                    if self.start_button.is_clicked(pygame.mouse.get_pos()):
                        self.start_game()  # Restart the game when start button is clicked
                    elif self.ranking_button.is_clicked(pygame.mouse.get_pos()):
                        self.show_ranking()  # Show ranking when ranking button is clicked
            if event.type == pygame.KEYDOWN and self.game_started:  # Only handle key events when the game is started
                if event.key == pygame.K_SPACE:
                    self.player.jump()
        return True

    
    def start_game(self):
        self.game_started = True
        self.score = 0
        self.player.rect.y = HEIGHT // 2 - 25
        self.player.vel = 0  # Reset player's velocity
        self.obstacles = []
        self.game_over = False
        self.create_start_button()  # Create a new start button
        self.create_ranking_button()  # Create a new ranking button


    def update(self):
        if self.game_started:
            self.player.rect.y += self.player.vel
            self.player.vel += 1

            if self.player.rect.y <= 0 or self.player.rect.y + self.player.rect.height >= HEIGHT:
                self.end_game()

            if len(self.obstacles) == 0 or self.obstacles[-1].rect.x < WIDTH - 200:
                self.generate_obstacle()

            for obstacle in self.obstacles:
                obstacle.rect.x -= 5
                if obstacle.rect.colliderect(self.player.rect) and not obstacle.collided:
                    obstacle.collided = True
                    self.score += 1

                if obstacle.rect.x + obstacle.rect.width < self.player.rect.x and not obstacle.collided:
                    obstacle.collided = True
                    self.score += 1

                if obstacle.rect.colliderect(self.player.rect):
                    self.end_game()

            self.obstacles = [obstacle for obstacle in self.obstacles if obstacle.rect.x + obstacle.rect.width > 0]

        return True

    def draw(self):
        WIN.fill(BLACK)
        self.player.draw(WIN)
        for obstacle in self.obstacles:
            obstacle.draw(WIN)
        self.draw_score()
        if not self.game_started:
            if not self.game_over:
                self.start_button.draw(WIN, WHITE)
            else:
                self.start_button.draw(WIN, WHITE)
                if self.ranking_button:
                    self.ranking_button.draw(WIN, WHITE)  # Draw ranking button if it exists
        pygame.display.update()

    def end_game(self):
        self.game_started = False
        self.game_over = True
        self.best_scores.append(self.score)  # Add the current score to the list of all scores
        self.best_scores.sort(reverse=True)  # Sort the list of all scores in descending order
        self.best_scores = self.best_scores[:3]  # Update the best three scores
        
        # Reset the player's velocity for the next game
        self.player.vel = 0

        # Create new start and ranking buttons for the next game
        self.create_start_button()
        self.create_ranking_button()


    def create_start_button(self):
        button_width, button_height = 100, 50
        button_x = (WIDTH - button_width) // 2
        button_y = HEIGHT // 2 - button_height - self.button_gap // 2
        self.start_button = Button(button_x, button_y, button_width, button_height, GRAY, 'Start')

    def create_ranking_button(self):
        button_width, button_height = 100, 50
        button_x = (WIDTH - button_width) // 2
        button_y = HEIGHT // 2 + self.button_gap * 2
        self.ranking_button = Button(button_x, button_y, button_width, button_height, GRAY, 'Ranking')

    def show_ranking(self):
        ranking = self.best_scores  # Get the best three scores
        while len(ranking) < 3:  # Fill the remaining slots with zeros if needed
            ranking.append(0)
        ranking_screen = True
        while ranking_screen:
            WIN.fill(BLACK)
            font = pygame.font.SysFont('comicsans', 40)
            title = font.render('Best Scores', 1, WHITE)
            WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
            for i, score in enumerate(ranking):
                text = font.render(str(score), 1, WHITE)
                WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, 150 + i * 50))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ranking_screen = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    ranking_screen = False

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
