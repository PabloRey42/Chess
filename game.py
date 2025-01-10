import pygame

pygame.init()

pygame.display.set_mode((400,400))

clock = pygame.time.Clock()


def main():
    running = True
    fps = 60
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
pygame.quit()