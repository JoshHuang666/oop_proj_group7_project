import pygame
import os

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Selection")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
BLUE = (0, 0, 255)

# Load background music
audio_path = os.path.join(os.path.dirname(__file__), 'final/audio')  # Path to the 'audio' directory
background_music_a = os.path.join(audio_path, 'background_a.wav')
background_music_b = os.path.join(audio_path, 'background_b.wav')
background_music_c = os.path.join(audio_path, 'background_c.wav')

# Adjust volume
pygame.mixer.music.set_volume(0.5)  # Set the initial volume to 50%

def play_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)  # Play the background music indefinitely

def stop_music():
    pygame.mixer.music.stop()

def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        WIN.fill(WHITE)

        # Display buttons
        stop_button = pygame.Rect(WIDTH - 100, 10, 80, 30)
        pygame.draw.rect(WIN, GRAY, stop_button)
        stop_text = pygame.font.SysFont(None, 24).render('Stop', True, BLACK)
        WIN.blit(stop_text, stop_button.center)

        song_buttons = []
        song_names = ['Song A', 'Song B', 'Song C']
        for i, song_name in enumerate(song_names):
            button_rect = pygame.Rect(50, 50 + i * 40, 150, 30)
            pygame.draw.rect(WIN, GRAY, button_rect)
            song_text = pygame.font.SysFont(None, 24).render(song_name, True, BLACK)
            WIN.blit(song_text, button_rect.center)
            song_buttons.append(button_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if stop_button.collidepoint(event.pos):
                    stop_music()
                for i, button_rect in enumerate(song_buttons):
                    if button_rect.collidepoint(event.pos):
                        if i == 0:
                            play_music(background_music_a)
                        elif i == 1:
                            play_music(background_music_b)
                        elif i == 2:
                            play_music(background_music_c)

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()

