import pygame
import random

pygame.init()


class Catch:
    def __init__(self):
        self.screen_width = 400
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Catch")
        self.screen.fill((0, 0, 0))

        self.background_sprite_speed = 5
        self.background_sprite = pygame.image.load('background.png').convert_alpha()
        self.background_sprite_topleft = 0
        self.background_sprite_bottomleft = -600

        self.player_sprite_size = 32
        self.player_surface = pygame.image.load("fox.png")
        self.player_sprite = pygame.sprite.Sprite()
        self.player_sprite.image = self.player_surface
        self.player_sprite.rect = self.player_surface.get_rect()
        self.player_sprite.rect.x = self.screen_width / 2 - (self.player_sprite_size / 2)
        self.player_sprite.rect.y = self.screen_height - (self.player_sprite_size * 2)

        self.target_sprite_size = 32
        self.target_surface = pygame.image.load("target.png")

        self.font = pygame.font.SysFont("Arial", 32)
        self.score = 0

        self.player_move_speed = 6
        self.moving_left = False
        self.moving_right = False
        self.clock = pygame.time.Clock()

        self.target_move_speed = 3
        self.target_sprite_group = pygame.sprite.Group()

        self.sprite_group = pygame.sprite.Group()
        self.sprite_group.add(self.player_sprite)
        self.sprite_group.draw(self.screen)

        pygame.display.flip()

    def create_target(self):
        target_sprite = pygame.sprite.Sprite()
        target_sprite.image = self.target_surface
        target_sprite.rect = self.target_surface.get_rect()
        target_sprite.rect.x = random.randint(self.target_sprite_size, self.screen.get_width() - self.target_sprite_size)
        target_sprite.rect.y = 0
        return target_sprite


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
        app.player_sprite.rect.x -= app.player_move_speed
    elif app.moving_right:
        app.player_sprite.rect.x += app.player_move_speed

    if pygame.time.get_ticks() % 60 == 0:
        target_object = app.create_target()
        app.target_sprite_group.add(target_object)

    for target in app.target_sprite_group.sprites():
        target.rect.y += app.target_move_speed

        if target.rect.y > app.screen.get_height():
            app.target_sprite_group.remove(target)

        if pygame.sprite.collide_rect(app.player_sprite, target):
            app.score += 1
            app.target_sprite_group.remove(target)

    app.screen.fill((0, 0, 0))
    app.background_sprite_topleft += app.background_sprite_speed
    app.background_sprite_bottomleft += app.background_sprite_speed

    if app.background_sprite_topleft >= app.screen_height:
        app.background_sprite_topleft = app.background_sprite_bottomleft - app.screen_height
    elif app.background_sprite_bottomleft >= app.screen_height:
        app.background_sprite_bottomleft = app.background_sprite_topleft - app.screen_height

    score_text = app.font.render(f"Score: {app.score}", True, (255, 255, 255))

    app.screen.blit(app.background_sprite, (0, app.background_sprite_topleft))
    app.screen.blit(app.background_sprite, (0, app.background_sprite_bottomleft))
    app.screen.blit(score_text, (100, 100))
    app.sprite_group.draw(app.screen)
    app.target_sprite_group.draw(app.screen)
    pygame.display.flip()

    app.clock.tick(60)

pygame.quit()
