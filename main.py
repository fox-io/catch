import pygame

pygame.init()


class Catch:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Catch")
        self.screen.fill((0, 0, 0))

        self.player_surface = pygame.image.load("fox.png")
        self.player_sprite = pygame.sprite.Sprite()
        self.player_sprite.image = self.player_surface
        self.player_sprite.rect = self.player_surface.get_rect()
        self.player_sprite.rect.x = 400-(32/2)
        self.player_sprite.rect.y = 600-64
        self.move_speed = 5
        self.moving_left = False
        self.moving_right = False

        self.sprite_group = pygame.sprite.Group()
        self.sprite_group.add(self.player_sprite)
        self.sprite_group.draw(self.screen)
        pygame.display.flip()


app = Catch()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                app.moving_left = True
            elif event.key == pygame.K_d:
                app.moving_right = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                app.moving_left = False
            elif event.key == pygame.K_d:
                app.moving_right = False

        if app.moving_left:
            app.player_sprite.rect.x -= app.move_speed
        elif app.moving_right:
            app.player_sprite.rect.x += app.move_speed

        app.screen.fill((0, 0, 0))
        app.sprite_group.draw(app.screen)
        pygame.display.update()

pygame.quit()
