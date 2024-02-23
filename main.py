import pygame
import random

pygame.init()


class Target:
    IMAGE = pygame.image.load('assets/target.png')
    SIZE = 32  # Size in pixels of target image
    SPEED = 3  # Speed at which target moves
    STATUS = {'OFF_SCREEN': 0, 'HIT_PLAYER': 1, 'OK': 2}

    def __init__(self, window):
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.IMAGE
        self.sprite.rect = self.IMAGE.get_rect()
        # Assign a random value (within screen constraints) to the x coordinate of the sprite
        self.sprite.rect.x = random.randint(self.SIZE, window['WIDTH'] - self.SIZE)
        # Set the y coordinate of the sprite to 0
        self.sprite.rect.y = -32

    def on_update(self, window, player):
        self.sprite.rect.y += self.SPEED  # Move the sprite
        if self.sprite.rect.y > window['HEIGHT']:
            return self.STATUS['OFF_SCREEN']
        if pygame.sprite.collide_rect(player.sprite, self.sprite):
            return self.STATUS['HIT_PLAYER']
        return self.STATUS['OK']


class Player:
    # Shared Constants
    IMAGE = pygame.image.load('assets/fox.png')
    SIZE = 32  # Width of sprite
    SPEED = 6  # Speed at which player moves

    def __init__(self, window):
        # Configure the player sprite
        self.moving_left = False
        self.moving_right = False
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.IMAGE
        self.sprite.rect = self.IMAGE.get_rect()
        # Set player location to center of bottom of screen.
        self.sprite.rect.x = window['WIDTH'] / 2 - (self.SIZE / 2)
        self.sprite.rect.y = window['HEIGHT'] - (self.SIZE * 2)

    def on_update(self, window):
        # Move player if player is moving
        if self.moving_left:
            if self.sprite.rect.x > 0:
                self.sprite.rect.x -= self.SPEED
        elif self.moving_right:
            if self.sprite.rect.x < window['WIDTH'] - self.SIZE:
                self.sprite.rect.x += self.SPEED

    def on_event(self, e):
        # Enable or disable movement based on keyboard events
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a:
                self.moving_left = True
            elif e.key == pygame.K_d:
                self.moving_right = True
        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_a:
                self.moving_left = False
            elif e.key == pygame.K_d:
                self.moving_right = False


class Obstacle:
    # Shared Constants
    IMAGE = pygame.image.load('assets/tree.png')
    SIZE = 32  # Width of sprite
    SPEED = 3  # Speed at which obstacle moves
    STATUS = {'OFF_SCREEN': 0, 'HIT_PLAYER': 1, 'OK': 2}

    def __init__(self, window):
        # Create obstacle sprite
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = self.IMAGE
        self.sprite.rect = self.IMAGE.get_rect()

        # Randomly assign the x-axis spawn point. y-axis is -32 to spawn off-screen
        self.sprite.rect.x = random.randint(self.SIZE, window['WIDTH'] - self.SIZE)
        self.sprite.rect.y = -32

    def on_update(self, window, player):
        # Move obstacle
        self.sprite.rect.y += self.SPEED

        # Check if obstacle is off-screen
        if self.sprite.rect.y > window['HEIGHT']:
            return self.STATUS['OFF_SCREEN']

        # Check if obstacle has hit player
        if pygame.sprite.collide_rect(player.sprite, self.sprite):
            return self.STATUS['HIT_PLAYER']

        # Return self.OK if obstacle is still in play
        return self.STATUS['OK']


class Background:
    # Constants
    IMAGE = pygame.image.load('assets/background.png')
    SPEED = 3

    def __init__(self, window):
        self.location_one = 0
        self.location_two = window["HEIGHT"] * -1

    def on_update(self, window):
        # Move background to new location
        self.location_one += self.SPEED
        self.location_two += self.SPEED

        # If background is off-screen, move it to the top of the screen
        if self.location_one >= window["HEIGHT"]:
            self.location_one = self.location_two - window["HEIGHT"]
        elif self.location_two >= window["HEIGHT"]:
            self.location_two = self.location_one - window["HEIGHT"]


class Score:
    COLORS = {'WHITE': (255, 255, 255)}

    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 32)
        self.score = 0

    def on_update(self):
        # Prevent negative scores
        if self.score < 0:
            self.score = 0
        self.text = self.font.render(f"Score: {self.score}", True, self.COLORS['WHITE'])


class Game:
    # Constants
    WINDOW = {'WIDTH': 400, 'HEIGHT': 600, 'TITLE': "Catch"}
    TIMER = {'SPAWN': 1000}

    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.targets = []
        self.obstacles = []
        # Pygame Screen Variables
        self.screen = pygame.display.set_mode((self.WINDOW['WIDTH'], self.WINDOW['HEIGHT']))
        pygame.display.set_caption(self.WINDOW['TITLE'])

        self.bg = Background(self.WINDOW)
        self.score = Score()
        self.player = Player(self.WINDOW)
        self.sprites.add(self.player.sprite)

        # Clock
        self.clock = pygame.time.Clock()

        # Target Creation Timer
        pygame.time.set_timer(pygame.USEREVENT, self.TIMER['SPAWN'])

        self.on_update()

    def on_update(self):
        # Process updates for Player.
        self.player.on_update(self.WINDOW)

        # Process updates for Targets.  Remove targets that are off-screen.
        for target in self.targets:
            target_status = target.on_update(self.WINDOW, self.player)
            if target_status == target.STATUS['OFF_SCREEN']:
                self.targets.remove(target)
                self.sprites.remove(target.sprite)
                # Lose one point if target is missed
                self.score.score -= 1
            elif target_status == target.STATUS['HIT_PLAYER']:
                self.targets.remove(target)
                self.sprites.remove(target.sprite)
                # Gain one point if target is caught
                self.score.score += 1

        # Process updates for Obstacles.  Remove obstacles that are off-screen.
        for obstacle in self.obstacles:
            obstacle_status = obstacle.on_update(self.WINDOW, self.player)
            if obstacle_status == obstacle.STATUS['OFF_SCREEN']:
                self.obstacles.remove(obstacle)
                self.sprites.remove(obstacle.sprite)
            elif obstacle_status == obstacle.STATUS['HIT_PLAYER']:
                self.obstacles.remove(obstacle)
                self.sprites.remove(obstacle.sprite)
                # Lose all points if obstacle is hit
                self.score.score = 0

        self.bg.on_update(self.WINDOW)
        self.score.on_update()

        # Blit Sprites
        self.screen.blit(self.bg.IMAGE, (0, self.bg.location_one))
        self.screen.blit(self.bg.IMAGE, (0, self.bg.location_two))
        self.sprites.draw(self.screen)

        self.screen.blit(self.score.text, (100, 100))

        # Update Screen
        pygame.display.flip()

    def on_event(self, e):
        # Pass events to Player class
        self.player.on_event(e)
        # Exit Program if requested
        if e.type == pygame.QUIT:
            return False

        # Create Targets and obstacles Every x Seconds
        if e.type == pygame.USEREVENT:
            new_target = Target(self.WINDOW)
            self.targets.append(new_target)
            self.sprites.add(new_target.sprite)

            new_obstacle = Obstacle(self.WINDOW)
            self.obstacles.append(new_obstacle)
            self.sprites.add(new_obstacle.sprite)

        # Continue Running
        return True


# Create App
app = Game()

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        # Run until event handler returns False
        running = app.on_event(event)

    # Update screen every frame
    app.on_update()

    # Keep clock at 60 fps
    app.clock.tick(60)

# End Program
pygame.quit()
