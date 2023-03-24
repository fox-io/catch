import pygame

pygame.init()


class Catch:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Catch")

        self.screen.fill((0, 0, 0))
        pygame.display.flip()


app = Catch()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
