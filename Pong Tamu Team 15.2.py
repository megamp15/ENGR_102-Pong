# By submitting this assignment, all team members agree to the following:
#  “Aggies do not lie, cheat, or steal, or tolerate those who do”
#  “I have not given or received any unauthorized aid on this assignment”
#
# Names:      	Mahir Pirmohammed
# 	        	Garrett Mason
# 	        	Tim Wagner
#             	Asad Ali
# Section:    	528
# Assignment: 	Team Project - PONG Team 15
# Date:       	12/7/15
from pygame.locals import *
from AI import *
from misc import*

enemy_ai = Enemy_AI(AI_MIN_REACT, AI_MAX_REACT, AI_HIT_ZONE_MIN, AI_HIT_ZONE_MAX)

def main():
    run = 1
    while run == 1:
        # the constants that are used
        WINSIZE = [800, 600]
        WHITE = [255, 255, 255]
        BLACK = [0, 0, 0]
        RED = [255, 0, 0]
        GREEN = [0, 255, 0]
        BLUE = [0, 0, 255]
        MAROON = [128,0,0]
        INDIANRED = [205,92,92]
        MAXX = 780
        MINX = 20
        MAXY = 580
        MINY = 0
        TRUE = 1
        FALSE = 0
        LEFT = 1
        RIGHT = 0
        PADDLESTEP = 4  # was 3

        # VARIABLES
        paddleleftxy = [5, 200]
        paddlerightxy = [775, 200]
        gameover = TRUE
        ballxy = [200, 200]

        ballspeed = 2
        balldy = 1
        balldx = 1

        ballservice = TRUE
        service = LEFT
        scoreleft = 0
        scoreright = 0

        ballcludge = 0  # added for problems that had occured with right paddle

        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(WINSIZE)
        pygame.display.set_caption('PONG TAMU 2018')
        screen.fill(BLACK)
        paddle = pygame.image.load('paddle.bmp').convert()
        paddleerase = pygame.image.load('paddleerase.bmp').convert()
        ball = pygame.image.load('ball.bmp').convert()
        ballerase = pygame.image.load('ballerase.bmp').convert()

        # title screen

        while gameover == TRUE:

            font = pygame.font.SysFont("arial black", 32)
            text_surface = font.render("PONG TAMU 2018 Team 15", True, MAROON)
            screen.blit(text_surface, (80, 40))
            text_surface = font.render("Left paddle A and Z to move", True, INDIANRED)
            screen.blit(text_surface, (80, 120))
            text_surface = font.render("Right paddle UP and DOWN to move", True, INDIANRED)
            screen.blit(text_surface, (80, 160))
            text_surface = font.render("S or RETURN to serve the ball", True, INDIANRED)
            screen.blit(text_surface, (80, 200))
            text_surface = font.render("P to pause, R to resume, Q to quit", True, INDIANRED)
            screen.blit(text_surface, (80, 240))
            text_surface = font.render("Press N to play with two players", True, INDIANRED)
            screen.blit(text_surface, (80, 280))
            text_surface = font.render("Press T to play against computer", True, INDIANRED)
            screen.blit(text_surface, (80, 320))
            text_surface = font.render(" - user on left and computer on right", True, RED)
            screen.blit(text_surface, (90, 360))
            text_surface = font.render(" BEST TO 15 ", True, BLUE)
            screen.blit(text_surface, (80, 420))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()

            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_n]:
                gameover = FALSE
                screen.fill(BLACK)
            elif pressed_keys[K_t]:
                random.seed(None)
                pygame.init()

                if not pygame.font.get_init():
                    print('Pygame: Font module failed to load.')
                if not pygame.mixer.get_init():
                    print('Pygame: Mixer module failed to load.')
                if not pygame.display.get_init():
                    print('Pygame: Display module failed to load.')

                enemy_ai = Enemy_AI(AI_MIN_REACT, AI_MAX_REACT, AI_HIT_ZONE_MIN, AI_HIT_ZONE_MAX)

                # sound objects
                bat_hit_snd = pygame.mixer.Sound(BAT_HIT_SND)
                wall_hit_snd = pygame.mixer.Sound(WALL_HIT_SND)
                score_snd = pygame.mixer.Sound(SCORE_SND)
                point_lost_snd = pygame.mixer.Sound(POINT_LOST_SND)

                # Game objects
                screen_info = Screen(SCREEN_WIDTH, SCREEN_HEIGHT)
                paddle1 = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE1_START_X, PADDLE1_START_Y,
                                 PADDLE_SPEED, screen_info, obj_color=GREEN)
                paddle2 = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE2_START_X, PADDLE2_START_Y,
                                 PADDLE_SPEED, screen_info, obj_color=GREEN)
                ball = Ball(BALL_WIDTH, BALL_START_X, BALL_START_Y, BALL_SPEED, screen_info,
                            bat_hit_snd, wall_hit_snd, score_snd, point_lost_snd, obj_color=YELLOW)

                clock = pygame.time.Clock()

                SCREEN = pygame.display.set_mode(SCREEN_SIZE)

                # prepare display surface
                pygame.display.set_caption(CAPTION_TEXT)
                SCREEN.fill(BLACK)
                SCREEN.convert_alpha()

                # get surfaces for paddles and ball
                paddle1_surface = paddle1.get_surface()
                paddle2_surface = paddle2.get_surface()
                ball_surface = ball.get_surface()

                # game state variables
                done = False
                in_play = False
                elapsed = 0.0
                show_stats = False
                decoy = None

                # Main game loop for  player vs ai or player vs computer
                while not done:
                    seconds = elapsed / 1000.0
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            done = True
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q:
                                done = True
                            if event.key == pygame.K_UP:
                                paddle1.y_vel = -1
                            if event.key == pygame.K_DOWN:
                                paddle1.y_vel = 1
                            if event.key == pygame.K_RETURN and not in_play:
                                ball.x_vel = random.choice([1, -1])
                                ball.y_vel = random.choice([1, -1])
                                enemy_ai.set_reaction_time()
                                in_play = True
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                                paddle1.y_vel = 0

                    if enemy_ai.focused:
                        if abs(paddle2.y_pos - ball.y_pos) < 50 and ball.x_pos < 100:
                            paddle2.y_vel = enemy_ai.update(paddle2, ball)
                        else:
                            paddle2.y_vel = enemy_ai.update(paddle2, decoy)
                        if ball.x_vel > 0:
                            enemy_ai.focused = False
                            decoy = None
                    else:
                        if ball.x_vel <= -1 and (ball.y_vel > 1 or ball.y_vel < -1):
                            decoy = enemy_ai.focus(ball, paddle1, paddle2, seconds)
                        paddle2.y_vel = enemy_ai.update(paddle2, ball)
                    if ball.x_vel == 0 and ball.y_vel == 0:
                        paddle2.y_vel = enemy_ai.update(paddle2, ball)

                    if ball.is_dead_ball(paddle1, paddle2):
                        enemy_ai.unfocus()
                        decoy = None
                        ball = Ball(BALL_WIDTH, BALL_START_X, BALL_START_Y, BALL_SPEED,
                                    screen_info, bat_hit_snd, wall_hit_snd, score_snd, point_lost_snd)
                        if paddle1.score == 15:
                            font = pygame.font.SysFont("arial", 64)
                            game_surface = font.render("Ai WINS!!", True, BLUE)
                            game_rect = screen.blit(game_surface, (250, 250))
                            pygame.display.update()
                            pygame.draw.rect(screen, BLACK, game_rect)
                            exit()
                        elif paddle2.score == 15:
                            font = pygame.font.SysFont("arial", 64)
                            player_surface = font.render("Player wins!!", True, BLUE)
                            player_rect = screen.blit(player_surface, (250, 250))
                            pygame.display.update()
                            pygame.draw.rect(screen, BLACK, player_rect)
                            exit()
                        in_play = False
                    pressed_keys = pygame.key.get_pressed()
                    if pressed_keys[K_p]:
                        gamepaused = TRUE
                        font = pygame.font.SysFont("arial", 64)
                        paused_surface = font.render("PAUSED \n R to resume", True, BLUE)
                        paused_rect = screen.blit(paused_surface, (150, 250))
                        pygame.display.update()

                        while gamepaused == TRUE:

                            for event in pygame.event.get():
                                if event.type == QUIT:
                                    exit()

                            pressed_keys = pygame.key.get_pressed()

                            if pressed_keys[K_r]:
                                gamepaused = FALSE
                            clock.tick(20)
                            pygame.draw.rect(screen, BLACK, paused_rect)

                    # Draw to game
                    SCREEN.fill(BLACK)
                    SCREEN.blit(paddle1_surface, paddle1.get_position(seconds))
                    SCREEN.blit(paddle2_surface, paddle2.get_position(seconds))
                    SCREEN.blit(ball_surface, ball.get_position(paddle1, paddle2, seconds))

                    # draw text
                    font = pygame.font.SysFont("arial", 64)
                    SCREEN.blit(font.render(str(paddle1.score), 0, BLUE),
                                (SCREEN_WIDTH / 8, SCREEN_HEIGHT - 520))
                    SCREEN.blit(font.render(str(paddle2.score), 0, BLUE),
                                (SCREEN_WIDTH - (SCREEN_WIDTH / 8), SCREEN_HEIGHT - 520))
                    if show_stats:
                        SCREEN.blit(font.render('HIT-ZONE: ' + str(enemy_ai.hit_zone) + ' REACT: ' + \
                                                str(enemy_ai.reaction_time), 0, WHITE), (50, 100))
                        if enemy_ai.focused:
                            SCREEN.blit(font.render('FOCUSED', 0, WHITE), (50, 50))
                            SCREEN.blit(
                                font.render('AI PADDLE: ' + str(int(paddle2.x_pos)) + ', ' + str(int(paddle2.y_pos)),
                                            0, WHITE), (50, 25))
                        if decoy is not None:
                            SCREEN.blit(font.render(
                                'Expected intercept: ' + str(int(decoy.x_pos)) + ', ' + str(int(decoy.y_pos)),
                                0, WHITE), (300, 25))

                    pygame.display.flip()
                    elapsed = clock.tick(FPS)

                pygame.quit()
            elif pressed_keys[K_q]:
                run = 0
                exit()

            clock.tick(20)

        # main game loop for user vs user or player vs player

        while not gameover:

            # clear screen on paddles and ball and print scores

            screen.blit(paddleerase, paddleleftxy)
            screen.blit(paddleerase, paddlerightxy)
            screen.blit(ballerase, ballxy)

            font = pygame.font.SysFont("arial", 64)
            text_surface1 = font.render(str(scoreleft), True, BLUE)
            textleft = screen.blit(text_surface1, (40, 40))
            text_surface1 = font.render(str(scoreright), True, BLUE)
            textright = screen.blit(text_surface1, (700, 40))

            # parse input events and move paddles

            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()

            pressed_keys = pygame.key.get_pressed()
            try: # capturing any run time errors due to user input
                if pressed_keys[K_a]:
                    if paddleleftxy[1] > MINY:
                        paddleleftxy[1] = paddleleftxy[1] - PADDLESTEP

                elif pressed_keys[K_z]:
                    if paddleleftxy[1] < MAXY - 80:
                        paddleleftxy[1] = paddleleftxy[1] + PADDLESTEP

                if pressed_keys[K_UP]:
                    if paddlerightxy[1] > MINY:
                        paddlerightxy[1] = paddlerightxy[1] - PADDLESTEP

                elif pressed_keys[K_DOWN]:
                    if paddlerightxy[1] < MAXY - 80:
                        paddlerightxy[1] = paddlerightxy[1] + PADDLESTEP
            except:
                font = pygame.font.SysFont("arial", 64)
                incorrect_surface = font.render("INVALID INPUT TRY AGAIN", True, BLUE)
                incorrect_rect = screen.blit(incorrect_surface, (150, 250))
                pygame.display.update()
                pygame.draw.rect(screen, BLACK, incorrect_rect)

            # serve the ball if we are serving !
            if (pressed_keys[K_s] or pressed_keys[K_RETURN]) and ballservice == TRUE:
                ballservice = FALSE
                if service == LEFT:
                    # introduce random ball direction on serve
                    balldx = random.randrange(2, 3)
                    balldy = random.randrange(-3, 3)
                    service = RIGHT
                else:
                    # introduce random ball direction on serve
                    balldx = random.randrange(2, 3)
                    balldy = random.randrange(-3, 3)
                    service == LEFT

            if pressed_keys[K_q]:
                run = 0
                exit()

            if pressed_keys[K_p]:
                gamepaused = TRUE
                font = pygame.font.SysFont("arial", 64)
                paused_surface = font.render("PAUSED \n R to resume", True, BLUE)
                paused_rect = screen.blit(paused_surface, (150, 250))
                pygame.display.update()

                while gamepaused == TRUE:

                    for event in pygame.event.get():
                        if event.type == QUIT:
                            exit()

                    pressed_keys = pygame.key.get_pressed()

                    if pressed_keys[K_r]:
                        gamepaused = FALSE
                    clock.tick(20)

                pygame.draw.rect(screen, BLACK, paused_rect)

            # if not serving just move the ball
            if ballservice is not TRUE:
                # have we hit the left paddle
                if ballxy[0] < (paddleleftxy[0] + 20) and ballxy[1] > (paddleleftxy[1] - 18) and ballxy[1] < (paddleleftxy[1] + 98):
                    balldx = -balldx
                    if pressed_keys[K_a] or pressed_keys[K_z]:
                        balldy = random.randrange(2, 4)
                    else:
                        balldy = random.randrange(0, 3)

                # have we hit the right paddle
                elif ballxy[0] > (paddlerightxy[0] - 20) and ballxy[1] > (paddlerightxy[1] - 18) and ballxy[1] <= (paddlerightxy[1] + 98):
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
                ballxy[0] = ballxy[0] + (ballspeed * balldx)
                ballxy[1] = ballxy[1] + (ballspeed * balldy)

            #  if we are serving set up the ball by the paddle
            else:
                if service == LEFT:
                    ballxy[0] = paddleleftxy[0] + 25
                    ballxy[1] = paddleleftxy[1] + 40
                elif service == RIGHT:
                    ballxy[0] = paddlerightxy[0] - 25
                    ballxy[1] = paddlerightxy[1] + 40
            # RENDER SCREEN
            if scoreleft == 15:
                font = pygame.font.SysFont("arial", 64)
                game_surface = font.render("LEFT PLAYER WINS!!", True, BLUE)
                game_rect = screen.blit(game_surface, (250, 250))
                pygame.display.update()
                pygame.draw.rect(screen, BLACK, game_rect)
                exit()
            elif scoreright == 15:
                font = pygame.font.SysFont("arial", 64)
                player_surface = font.render("RIGHT PLAYER WINS!!", True, BLUE)
                player_rect = screen.blit(player_surface, (250, 250))
                pygame.display.update()
                pygame.draw.rect(screen, BLACK, player_rect)
                exit()

            screen.blit(paddle, paddleleftxy)
            screen.blit(paddle, paddlerightxy)
            screen.blit(ball, ballxy)
            pygame.display.update()

            clock.tick(300)


if __name__ == '__main__':
    main()
# game runs !!!!!