import pygame
import random

pygame.init()


class Catch:
    def __init__(self):
        # Pygame Screen Variables
        self.screen_width = 400
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Catch")

        # Background Sprite Variables
        self.background_sprite_speed = 5
        self.background_sprite = pygame.image.load('background.png').convert_alpha()
        self.background_sprite_topleft = 0
        self.background_sprite_bottomleft = -600

        # Player Sprite Variables
        self.player_sprite_size = 32
        self.player_surface = pygame.image.load("fox.png")
        self.player_sprite = pygame.sprite.Sprite()
        self.player_sprite.image = self.player_surface
        self.player_sprite.rect = self.player_surface.get_rect()
        self.player_sprite.rect.x = self.screen_width / 2 - (self.player_sprite_size / 2)
        self.player_sprite.rect.y = self.screen_height - (self.player_sprite_size * 2)
        self.player_move_speed = 6
        self.moving_left = False
        self.moving_right = False
        self.sprite_group = pygame.sprite.Group()
        self.sprite_group.add(self.player_sprite)
        self.sprite_group.draw(self.screen)

        # Target Sprite Variables
        self.target_sprite_size = 32
        self.target_surface = pygame.image.load("target.png")
        self.target_move_speed = 3
        self.target_sprite_group = pygame.sprite.Group()

        # Font Variables
        self.font = pygame.font.SysFont("Arial", 32)

        # Score Variables
        self.score = 0

        # Clock Variables
        self.clock = pygame.time.Clock()

        self.update_screen()

    def update_screen(self):
        # Move player if player is moving
        if self.moving_left:
            self.player_sprite.rect.x -= self.player_move_speed
        elif self.moving_right:
            self.player_sprite.rect.x += self.player_move_speed

        # Add target every 60 ticks
        if pygame.time.get_ticks() % 60 == 0:
            target_object = self.create_target()
            self.target_sprite_group.add(target_object)

        # Move targets and check for collisions
        for target in self.target_sprite_group.sprites():
            target.rect.y += self.target_move_speed

            if target.rect.y > self.screen.get_height():
                self.target_sprite_group.remove(target)

            if pygame.sprite.collide_rect(self.player_sprite, target):
                self.score += 1
                self.target_sprite_group.remove(target)

        # Move background
        self.background_sprite_topleft += self.background_sprite_speed
        self.background_sprite_bottomleft += self.background_sprite_speed

        # Loop background
        if self.background_sprite_topleft >= self.screen_height:
            self.background_sprite_topleft = self.background_sprite_bottomleft - self.screen_height
        elif self.background_sprite_bottomleft >= self.screen_height:
            self.background_sprite_bottomleft = self.background_sprite_topleft - self.screen_height

        # Create Update Score Text
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))

        # Blit Sprites
        self.screen.blit(self.background_sprite, (0, self.background_sprite_topleft))
        self.screen.blit(self.background_sprite, (0, self.background_sprite_bottomleft))
        self.sprite_group.draw(self.screen)
        self.target_sprite_group.draw(self.screen)
        self.screen.blit(score_text, (100, 100))

        # Update Screen
        pygame.display.flip()

    def create_target(self):
        target_sprite = pygame.sprite.Sprite()
        target_sprite.image = self.target_surface
        target_sprite.rect = self.target_surface.get_rect()
        target_sprite.rect.x = random.randint(self.target_sprite_size, self.screen.get_width() - self.target_sprite_size)
        target_sprite.rect.y = 0
        return target_sprite

    def event_handler(self, e):
        # Exit Program if requested
        if e.type == pygame.QUIT:
            return False
        # Handle Keyboard Input
        elif e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
            self.moving_left = e.type == pygame.KEYDOWN and e.key == pygame.K_a and True or False
            self.moving_right = e.type == pygame.KEYDOWN and e.key == pygame.K_d and True or False

        # Continue Running
        return True


# Create App
app = Catch()

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        # Run until event handler returns False
        running = app.event_handler(event)

    app.update_screen()
    app.clock.tick(60)

# End Program
pygame.quit()
