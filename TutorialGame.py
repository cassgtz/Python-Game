import pygame
import random
# keys used in this game
from pygame.locals import (
    RLEACCEL,  # a constant that we can pass in as parameter to help load things quicker
    K_UP,
    K_DOWN,
    K_RIGHT,
    K_LEFT,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)
# initialize pygame
pygame.init()
# set up for sounds
pygame.mixer.init()
pygame.mixer.music.load("assets/Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)  # never ends
shoot_sound = pygame.mixer.Sound("assets/Shoot.ogg")
collision_sound = pygame.mixer.Sound("assets/Collision.mp3")
power_sound = pygame.mixer.Sound("assets/powerup.ogg")

# set up screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Sprite: 2D representation of something on the screen
# In pygame there is a Sprite class that's designed to hold one or several representations
# of any game objects that you want to display on the screen
# For each type of object you have, you could make a class for that object & extends Sprite from pygame
# using inheritance to inherit from the built-in Sprite class to make our Sprites
# Classes for this game: enemy (missiles), cloud, player (jet), bullet, power(piggy).


# Define Enemy class by extending from Sprite class
class Enemy (pygame.sprite.Sprite):
    # take a number as parameter to define speed so we can alter it later based on level
    def __init__(self, number):
        super(Enemy, self).__init__() # calling the init function from Sprite class
        self.surf = pygame.image.load("assets/missile.png").convert() # load in image (missile)
        self.surf.set_colorkey((255, 255, 255), RLEACCEL) # set background color to be transparent
        self.rect = self.surf.get_rect(
            # have them pop up on screen at random locations
            center=(
                random.randint(SCREEN_WIDTH+10, SCREEN_WIDTH+50), # x location outside of screen view
                random.randint(0, SCREEN_HEIGHT) # random location on y axis
            )
        )
        self.speed = number

    # move all the way across screen from right to left
    def update(self):
        # move enemy based on speed
        self.rect.move_ip(-self.speed, 0)
        # remove this object once it flies off the screen
        if self.rect.right < 0:
            self.kill()  # removes the object


# Define a Player class by extending from Sprite class
# handle user control
class Player(pygame.sprite.Sprite):
    def __init__(self, width=75, height=25):
        super(Player, self).__init__()
        self.surf = pygame.image.load("assets/jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    # move player based on key pressed
    # take dictionary of pressed keys in parameter
    def update(self, pressed_keys, speed):
        if pressed_keys[K_UP]:
            # move_ip -> move in place
            # allows you to move current object
            self.rect.move_ip(0, -speed)
        elif pressed_keys[K_DOWN]:
            self.rect.move_ip(0, speed)
        elif pressed_keys[K_LEFT]:
            self.rect.move_ip(-speed, 0)
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(speed, 0)

        # keep our player inside of screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Define a Bullet class by extending from Sprite class
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        self.surf = pygame.image.load("assets/bullet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # bullet appears on screen at same location as jet's current location
        # set center of bullet to the location of the tip of the jet for "shooting out" effect
        middle = (player.rect.top + player.rect.bottom) / 2
        self.rect = self.surf.get_rect(
            center=(player.rect.right, middle)
        )

    # move all the way across screen from center to right & remove
    def update(self):
        self.rect.move_ip(4, 0)
        if self.rect.left < 0:
            self.kill()


# Define a Power class by extending from Sprite class
class Power(pygame.sprite.Sprite):
    def __init__(self):
        super(Power, self).__init__()
        self.surf = pygame.image.load("assets/piggy.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # randomly place them somewhere & move in from the right side of screen
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )

    # move from right to left & remove
    def update(self):
        self.rect.move_ip(-4, 0)
        if self.rect.right < 0:
            self.kill()


# Define a Cloud class by extending from Sprite class
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("assets/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # randomly place them somewhere & move in from the right side of screen
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )

    # move from right to left & remove
    def update(self):
        self.rect.move_ip(-4, 0)
        if self.rect.right < 0:
            self.kill()


# instantiate a Player object
player = Player()

# Grouping sprites
# Sprite group -> object that holds a group of Sprite objects
# using this makes it easier to check for collision

# Sprite groups for this game
# 1. A group that will hold every Sprite in the game
# 2. A group that holds all the enemy Sprites in the game
# 3. A group that holds all the cloud Sprites in the game
# 4. A group that holds all the bullet Sprites in the game
# 5. A group that holds all the power Sprites in the game

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# EVENTS
# pygame defines events as integer
# USEREVENT -> represents the last event
# define a new integer to create & represent custom events:

# add enemies
ADD_ENEMY = pygame.USEREVENT + 1
# Design is to add enemies to screen in time intervals
# set a timer to add event
pygame.time.set_timer(ADD_ENEMY, 350) # every 350 milliseconds we trigger a new add enemy event

# add clouds in time intervals
ADD_CLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_CLOUD, 1000)

# add powers every 40 seconds
ADD_POWER = pygame.USEREVENT + 3
pygame.time.set_timer(ADD_POWER, 40000)

# design is to level up every 30 seconds
LEVEL_UP = pygame.USEREVENT + 4
pygame.time.set_timer(LEVEL_UP, 30000)
# define variables for leveling up
enemy_speed = 1
level = 1

# Things your game loop should ALWAYS handle:
# 1. user interaction - press keys, type info, controller button smashing
# 2. update the states of all the game objects
# 3. update the display and other assets (ex: audio)
# 4. maintain the speed of the game

# each loop iteration/cycle is called a frame - frame rate
# the quicker you can do things each iteration, the faster your game will run
# frames will cont. to occur until some condition to quit is met
# set up a clock for frame rate
clock = pygame.time.Clock()
# define some variables for timer
font = pygame.font.Font('freesansbold.ttf', 30)
frame_count = 0
frame_rate = 60
start_time = 90

# Exit conditions for this game:
# 1. if the player collides with enemy w/o immunity
# 2. if the player closes window

safe = False
running = True
while running:
    # GAME EVENTS:
    # return list of events in the event queue
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            # if user presses space bar, add new bullet
            if event.key == K_SPACE:
                shoot_sound.play()
                newBullet = Bullet()
                bullets.add(newBullet)
                all_sprites.add(newBullet)
        # add new enemies
        elif event.type == ADD_ENEMY:
            # create a new enemy & add to groups
            newEnemy = Enemy(enemy_speed)
            enemies.add(newEnemy)
            all_sprites.add(newEnemy)
        # add new clouds
        elif event.type == ADD_CLOUD:
            newCloud = Cloud()
            clouds.add(newCloud)
            all_sprites.add(newCloud)
        # add new energizers
        elif event.type == ADD_POWER:
            newPower = Power()
            powers.add(newPower)
            all_sprites.add(newPower)
        # As levels increase, speed of enemies increase
        elif event.type == LEVEL_UP:
            level += 1
            enemy_speed += 1

    # DRAW EVERYTHING ONTO SCREEN:
    # Create surfaces and pass in a tuple of width & length
    # blit: how you copy the content onto another surface

    # fill background
    screen.fill((99, 184, 255))
    # blit all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    # call the update methods defined in classes to update their locations
    # grab all the keys that are currently pressed to pass in parameter for player
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys, 2)
    enemies.update()
    clouds.update()
    bullets.update()
    powers.update()

    # LEVELS:
    # format into Level X & blit on top center of screen
    level_count = "Level {}:".format(level)
    level_text = font.render(level_count, True, (255, 255, 255))
    screen.blit(level_text, [SCREEN_WIDTH - 465, SCREEN_HEIGHT - 595])

    # TIMER:
    # calculate minutes, seconds & format into 00:00
    minutes = (frame_count // frame_rate) // 60
    seconds = (frame_count // frame_rate) % 60
    timer = "{0:02}:{1:02}".format(minutes, seconds)
    # blit below level display
    timer_text = font.render(timer, True, (255, 255, 255))
    screen.blit(timer_text, [SCREEN_WIDTH-450, SCREEN_HEIGHT-560])

    # DETECT COLLISIONS:
    # if player collides with power, decrease the speed of enemies & kill flying pig
    # as the levels get higher, power provides a smaller decrease
    if pygame.sprite.spritecollideany(player, powers):
        power_sound.play()
        if 20 > enemy_speed >= 10:
            enemy_speed -= 1
        if 10 > enemy_speed >= 3:
            enemy_speed -= 2
        if enemy_speed == 2:
            enemy_speed = 1

    # if bullet collides with enemy, kill the enemy & the bullet
    if pygame.sprite.groupcollide(bullets, enemies, True, True):
        collision_sound.play()
    # if player collides with enemy, end the game
    if pygame.sprite.spritecollideany(player, enemies):
        collision_sound.play()
        player.kill()
        running = False

    pygame.display.flip()
    # ensure the game maintains a specific frame rate
    frame_count += 1
    clock.tick(frame_rate)

# once loop ends, stop the music & quit
pygame.mixer.music.stop()
pygame.mixer.quit()
