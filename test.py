import random, math, pygame
from pygame.locals import *
from AI import *
import random
from misc import*
pointcounter = 0

WINSIZE = [800, 600]
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
BLOCKSIZE = [20, 20]
MAXX = 780
MINX = 20
MAXY = 580
MINY = 0
BLOCKSTEP = 20
TRUE = 1
FALSE = 0
PADDLELEFTYVAL = 25
PADDLERIGHTYVAL = 775
LEFT = 1
RIGHT = 0
PADDLESTEP = 4  # was 3

        # VARIABLES
elapsed = 0.0
paddleleftxy = [5, 200]
paddlerightxy = [775, 200]
scoreleft = 0
scoreright = 0
gameover = TRUE
ballxy = [200, 200]

ballspeed = 2
balldy = 1
balldx = 1

ballservice = TRUE
service = LEFT
scoreleft = 0
scoreright = 0
ballcludge = 0  # added for problems with right paddle
textleft = [1, 1, 2, 2]
textright = [3, 3, 4, 4]

class Pong(object):
    def __init__(self, screensize):
        self.screensize = screensize

        self.centerx = int(screensize[0]*0.5)
        self.centery = int(screensize[1]*0.5)

        self.radius = 8

        self.rect = pygame.Rect(self.centerx-self.radius,
                            self.centery-self.radius,
                            self.radius*2, self.radius*2)

        self.color = (255,255,0)

        self.direction = [1,1]
        #speed of ball
        self.speedx = 5
        self.speedy = 5

        self.hit_edge_left = False
        self.hit_edge_right = False

    def update(self, player_paddle, ai_paddle):

        global pointcounter
        self.centerx += self.direction[0]*self.speedx
        self.centery += self.direction[1]*self.speedy

        self.rect.center = (self.centerx, self.centery)

        if self.rect.top <= 0:
            self.direction[1] = 1
        elif self.rect.bottom >= self.screensize[1]-1:
            self.direction[1] = -1

        if self.rect.right >= self.screensize[0]-1:
            self.hit_edge_right = True
        elif self.rect.left <= 0:
            self.hit_edge_left = True

        if self.rect.colliderect(player_paddle.rect):
            self.direction[0] = -1
            pointcounter += 1
        if self.rect.colliderect(ai_paddle.rect):
            self.direction[0] = 1

    def render(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius, 0)
        pygame.draw.circle(screen, (0,0,0), self.rect.center, self.radius, 1)

#creates the AI paddle
class AIPaddle(object):
    def __init__(self, screensize):
        self.screensize = screensize

        self.centerx = 5
        self.centery = int(screensize[1]*0.5)

        #ai paddle dimensions
        self.height = 100
        self.width = 45

        self.rect = pygame.Rect(0, self.centery-int(self.height*0.5),      self.width, self.height)

        self.color = (0,255,0)
        #ai paddle speed
        self.speed = 6

    def update(self, pong):
        if pong.rect.top < self.rect.top:
            self.centery -= self.speed
        elif pong.rect.bottom > self.rect.bottom:
            self.centery += self.speed

        self.rect.center = (self.centerx, self.centery)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)

#creates the player paddle
class PlayerPaddle(object):
    def __init__(self, screensize):
        self.screensize = screensize

        self.centerx = screensize[0]-5
        self.centery = int(screensize[1]*0.5)

        #player paddle dimensions
        self.height = 100
        self.width = 45

        self.rect = pygame.Rect(0, self.centery-int(self.height*0.5),     self.width, self.height)

        self.color = (0,255,0)

        #player paddle speed
        self.speed = 10
        self.direction = 0

    def update(self):
        self.centery += self.direction*self.speed

        self.rect.center = (self.centerx, self.centery)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screensize[1]-1:
            self.rect.bottom = self.screensize[1]-1

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)


def main():

    pygame.init()

    global pointcounter

    screensize = (640,480)

    screen = pygame.display.set_mode(screensize)

    clock = pygame.time.Clock()

    pong = Pong(screensize)
    ai_paddle = AIPaddle(screensize)
    player_paddle = PlayerPaddle(screensize)

    running = True

    while running:
        pressed_keys = pygame.key.get_pressed()
        clock.tick(64)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    player_paddle.direction = -1
                elif event.key == K_DOWN:
                    player_paddle.direction = 1
            if event.type == KEYUP:
                if event.key == K_UP and player_paddle.direction == -1:
                    player_paddle.direction = 0
                elif event.key == K_DOWN and player_paddle.direction == 1:
                    player_paddle.direction = 0

                    if ballxy[0] < (paddleleftxy[0] + 20) and ballxy[1] > (paddleleftxy[1] - 18) and ballxy[1] < (
                            paddleleftxy[1] + 98):
                        balldx = -balldx
                        if pressed_keys[K_a] or pressed_keys[K_z]:
                            balldy = random.randrange(2, 4)
                        else:
                            balldy = random.randrange(0, 3)

                    # have we hit the right paddle
                    elif ballxy[0] > (paddlerightxy[0] - 20) and ballxy[1] > (paddlerightxy[1] - 18) and ballxy[1] <= (
                            paddlerightxy[1] + 98):
                        # had to include ballcludge counter here to make sure ball did not bounce round paddle - Never seen
                        # any behaviour like this on the left paddle so not added there
                        if ballcludge == 0:
                            balldx = -balldx
                            if pressed_keys[K_UP] or pressed_keys[K_DOWN]:
                                balldy = random.randrange(2, 4)
                            else:
                                balldy = random.randrange(0, 3)
                            ballcludge = 1
                        else:
                            ballcludge = ballcludge + 1
                            if ballcludge == 4:
                                ballcludge = 0

                    # have we hit the top of screen
                    elif ballxy[1] <= MINY:
                        # 1#ballanglerad = -ballanglerad
                        balldy = -balldy
                    # have we hit the bottom of screen
                    elif ballxy[1] >= MAXY:
                        # 1#ballanglerad = -ballanglerad
                        balldy = -balldy
                    # have we passed the left paddle
                    elif ballxy[0] <= MINX:
                        ballservice = TRUE
                        service = RIGHT
                        scoreright = scoreright + 1
                        # clear the score right text
                        pygame.draw.rect(screen, BLACK, textright)
                    # have we passed the right paddle
                    elif ballxy[0] >= MAXX:
                        ballservice = TRUE
                        service = LEFT
                        scoreleft = scoreleft + 1
                        # clear the score left text
                        pygame.draw.rect(screen, BLACK, textleft)

                    # lets actually move the ball now we have the deltas
                    ballxy[0] = ballxy[0] + (ballspeed * 1)
                    ballxy[1] = ballxy[1] + (ballspeed * 1)
        ai_paddle.update(pong)
        player_paddle.update()
        pong.update(player_paddle, ai_paddle)



        screen.fill((0,0,0))

        ai_paddle.render(screen)
        player_paddle.render(screen)
        pong.render(screen)

        pygame.display.flip()



main()