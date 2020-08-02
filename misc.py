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

import pygame

# Misc Variables
AI_MAX_REACT = 10
AI_MIN_REACT = 20
AI_REACT_CEILING = 100
AI_HIT_ZONE_MIN = 5
AI_HIT_ZONE_MAX = 15

SCREEN_WIDTH = 780
SCREEN_HEIGHT = 580
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_SPEED = 300

BALL_WIDTH = 20
BALL_HEIGHT = 30
BALL_SPEED = 290

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255,255,0)
BLUE = (0,0,255)

PADDLE_GAP = 10

BAT_HIT_SND = 'bat_hit.wav'
WALL_HIT_SND = 'wall_hit.wav'
SCORE_SND = 'score_snd.wav'
POINT_LOST_SND = 'point_lost_snd.wav'

MUTE_INST_TEXT = "Press 'M' to mute the game."
START_INST_TEXT = "Press 'SPACE' to start a match."
MOVE_INST_TEXT = "Press 'UP' to move up and 'DOWN' to move down."
QUIT_INST_TEXT = "Press 'Q' to quit the game."

PADDLE1_START_X = SCREEN_WIDTH - PADDLE_WIDTH - PADDLE_GAP
PADDLE1_START_Y = SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2

PADDLE2_START_X = 0 + PADDLE_GAP
PADDLE2_START_Y = SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2

BALL_START_X = SCREEN_WIDTH / 20
BALL_START_Y = SCREEN_HEIGHT / 2
CAPTION_TEXT = "PONG"




class Screen(object):
    # A datatype for representing a display screen's width and height.
    def __init__(self, scr_width, scr_height):
        self.width = scr_width
        self.height = scr_height

class Pong_Object(object):
    # A base class for representing an object in a game of pong. """
    def __init__(self, w, h, x, y, move_speed, scr, obj_color=(255, 255, 255),
            alpha_color=(0, 0, 0)):

            # Pong_Object constructor:
                # w - width of the object.
                # h - height of the object.
                # x - the x position of the object.
                #y - the y position of the object.
                # move_speed - the speed at which the object moves.
                # scr - the screen the object will be drawn on.
                # obj_color - the color of the object
                # alpha_color - the color that will be transparent.

        self.width = w
        self.height = h
        self.x_pos = x
        self.y_pos = y
        self.color = obj_color
        self.alpha = alpha_color
        self.speed = move_speed
        self.x_vel = 0.0
        self.y_vel = 0.0
        self._screen_info = scr

    def get_size(self):
        # Returns a tuple containing the width and height of the object.
        return (self.width, self.height)

    def get_position(self, elapsed):
        # Returns a tuple containing the position of the object.
        # Will update the position of the object based on game state.

        self._update_position(elapsed)
        return (self.x_pos, self.y_pos)

    def _update_position(self, elapsed):
        # Updates the position of the object, based on its current velocity
        #and position.  this is where collision handling will occur.

        new_x = self._next_x_position(elapsed)
        new_y = self._next_y_position(elapsed)
        # Check if object is off the left of the screen
        if new_x < 0:
            self.x_pos = 0
        # Check if object is off the right of the screen
        elif new_x > self._screen_info.width - self.width:
            self.x_pos = self._screen_info.width - self.width
        else:
            self.x_pos = new_x
        # Check if object is off the top of the screen
        if new_y < 0:
            self.y_pos = 0
        # Check if object is off the bottom of the screen
        elif new_y > self._screen_info.height - self.height:
            self.y_pos = self._screen_info.height - self.height
        else:
            self.y_pos = new_y

    def _next_x_position(self, elapsed):
        # Returns the x position of the object after its next update.
        # Does not actually modify the object's position.

        return self.x_pos + self.x_vel * (self.speed * elapsed)

    def _next_y_position(self, elapsed):
        # Returns the y position of the object after its next update.
        # Does not actually modify the object's position.

        return self.y_pos + self.y_vel * (self.speed * elapsed)

class Paddle(Pong_Object):
    # A class for representing a paddle in pong.  Inherits from Pong_Object.
    def __init__(self, pad_width, pad_height, x, y, move_speed, screen,
            obj_color=(255,255,255)):
        Pong_Object.__init__(self, pad_width, pad_height, x, y, move_speed,
                screen, obj_color=obj_color)
        self.score = 0

    def get_surface(self):
        # Returns a surface for a paddle.  The surface will have the width
        # and height of the paddle object and will be colored white.

        surf = pygame.Surface(self.get_size())
        surf.fill(self.color)
        surf.convert_alpha()
        return surf

class Ball(Pong_Object):
    #  A class for representing a ball in pong.  Inherits from Pong_Object.
    def __init__(self, ball_diameter, x, y, move_speed, screen, bat_hit_sound, wall_hit_sound,
            score_sound, point_lost_sound, obj_color=(255, 255, 255)):
        Pong_Object.__init__(self, ball_diameter, ball_diameter, x, y,
                move_speed, screen, obj_color=obj_color)
        self.bat_hit_snd = bat_hit_sound
        self.wall_hit_snd = wall_hit_sound
        self.score_snd = score_sound
        self.point_lost_snd = point_lost_sound

    def copy(self):
        new_ball = Ball(self.width, self.x_pos, self.y_pos, self.speed,
                self._screen_info, None, None, None, None)
        new_ball.x_vel = self.x_vel
        new_ball.y_vel = self.y_vel
        return new_ball

    def get_position(self, p1, p2, elapsed):
        # Override the base class's get_position method so that we can pass in the
        # paddles.  This is necessary to handle collision with paddles.

        self.update_position(p1, p2, elapsed)
        return (self.x_pos, self.y_pos)

    def _check_for_paddle_collision(self, paddle1, paddle2, elapsed):
        # A private method for handling paddle collision. If the ball makes
        # contact with a paddle, its direction on the x axis will be reversed.

        new_x = self._next_x_position(elapsed)
        new_y = self._next_y_position(elapsed)
        # check if the ball will collide with the right paddle (player 1)
        if new_x > paddle1.x_pos-self.width and new_x < paddle1.x_pos + paddle1.width \
                and new_y > paddle1.y_pos and new_y < paddle1.y_pos + paddle1.height:
            delta_y = self.y_pos - (paddle1.y_pos + paddle1.height / 2)
            self.x_vel = -1
            self.y_vel = delta_y * 0.075 #+ (paddle1.y_vel / 2)
            if self.bat_hit_snd:
                self.bat_hit_snd.play()
        # check if the ball will collide with the left paddle (player 2)
        elif new_x < paddle2.x_pos + paddle2.width and new_x > paddle2.x_pos \
                and new_y > paddle2.y_pos and new_y < paddle2.y_pos + paddle2.height:
            delta_y = self.y_pos - (paddle2.y_pos + paddle2.height / 2)
            self.x_vel = 1
            self.y_vel = delta_y * 0.075 #+ (paddle2.y_vel / 2)
            if self.bat_hit_snd:
                self.bat_hit_snd.play()

    def _check_for_wall_collision(self, elapsed):
        #  A private method for handling wall collision. We only need to bounce off
        # the top and bottom of the screen.

        new_y = self._next_y_position(elapsed)
        # check for collision with the bottom of the screen
        if new_y > self._screen_info.height - self.height:
            self.y_vel *= -1
            if self.wall_hit_snd:
                self.wall_hit_snd.play()
        # check for collision with the top of the screen
        elif new_y < 0:
            self.y_vel *= -1
            if self.wall_hit_snd:
                self.wall_hit_snd.play()

    def update_position(self, p1, p2, elapsed):

        #Override the base class's update_position method so we can handle
        # ball/paddle collision.

        self._check_for_paddle_collision(p1, p2, elapsed)
        self._check_for_wall_collision(elapsed)
        self.x_pos = self._next_x_position(elapsed)
        self.y_pos  = self._next_y_position(elapsed)

    def get_surface(self):
        # Return a surface for the ball.  The surface will have the width and height
        # of the ball, will have a circle in the middle, and black will be set as the alpha
        # colorkey for transparency.

        surf = pygame.Surface(self.get_size())
        pygame.draw.circle(surf, self.color, (self.width // 2, self.height // 2),
                self.width // 2)
        surf.set_colorkey(self.alpha)
        surf.convert_alpha()
        return surf

    def is_dead_ball(self, paddle1, paddle2):
        # Returns True if the ball has gone outside the bounds of the screen.
        if self.x_pos > self._screen_info.width:
            self.point_lost_snd.play()
            paddle1.score += 1
            return True
        elif self.x_pos < 0:
            self.score_snd.play()
            paddle2.score += 1
            return True
        else:
            return False
