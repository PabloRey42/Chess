import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
HIGHLIGHT = (100, 100, 255)

# Fonts
FONT = pygame.font.Font(None, 74)
SMALL_FONT = pygame.font.Font(None, 36)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess Game")

def draw_text(text, font, color, surface, x, y):
    """Helper function to draw text on the screen."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def main_menu():
    """Displays the main menu."""
    while True:
        screen.fill(WHITE)

        # Title
        draw_text("Chess Game", FONT, BLACK, screen, SCREEN_WIDTH // 2, 100)

        # Menu options
        mx, my = pygame.mouse.get_pos()

        button_new_game = pygame.Rect(SCREEN_WIDTH // 2 - 150, 200, 300, 50)
        button_instructions = pygame.Rect(SCREEN_WIDTH // 2 - 150, 300, 300, 50)
        button_quit = pygame.Rect(SCREEN_WIDTH // 2 - 150, 400, 300, 50)

        pygame.draw.rect(screen, HIGHLIGHT if button_new_game.collidepoint((mx, my)) else GRAY, button_new_game)
        pygame.draw.rect(screen, HIGHLIGHT if button_instructions.collidepoint((mx, my)) else GRAY, button_instructions)
        pygame.draw.rect(screen, HIGHLIGHT if button_quit.collidepoint((mx, my)) else GRAY, button_quit)

        draw_text("New Game", SMALL_FONT, BLACK, screen, SCREEN_WIDTH // 2, 225)
        draw_text("Instructions", SMALL_FONT, BLACK, screen, SCREEN_WIDTH // 2, 325)
        draw_text("Quit", SMALL_FONT, BLACK, screen, SCREEN_WIDTH // 2, 425)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_new_game.collidepoint((mx, my)):
                    # Start new game
                    print("New Game Selected")
                    return "new_game"
                if button_instructions.collidepoint((mx, my)):
                    # Show instructions
                    print("Instructions Selected")
                    instructions_menu()
                if button_quit.collidepoint((mx, my)):
                    # Quit the game
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

def instructions_menu():
    """Displays the instructions menu."""
    while True:
        screen.fill(WHITE)

        draw_text("Instructions", FONT, BLACK, screen, SCREEN_WIDTH // 2, 100)
        draw_text("- Use the mouse to select pieces.", SMALL_FONT, BLACK, screen, SCREEN_WIDTH // 2, 200)
        draw_text("- Follow standard chess rules.", SMALL_FONT, BLACK, screen, SCREEN_WIDTH // 2, 250)
        draw_text("Press any key to return.", SMALL_FONT, BLACK, screen, SCREEN_WIDTH // 2, 350)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                return

        pygame.display.flip()

# Main loop
if __name__ == "__main__":
    main_menu()
