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
import random

random.seed(None)
PADDLE_GAP = 10
AI_MAX_REACT = 10
AI_MIN_REACT = 20
AI_REACT_CEILING = 100
AI_HIT_ZONE_MIN = 5
AI_HIT_ZONE_MAX = 15
BALL_SPEED = 200

class Enemy_AI(object):
    # This is a preliminary version of the enemy AI. It works by randomly
    # setting a reaction time which is just simply a number of frames that
    # must be drawn before the ai can act. This reaction time is a random
    # number between MIN_INTEL and MAX_INTEL. So if the reaction time is 15,
    # the ai will update its paddle's position every 15 frames.
    # The ai also will enter a 'focused' state if the ball is moving quickly enough,
    # in this state it abandons attempting to track the ball and instead attempts to
    # calculate the point at which it will meet the left wall of the game.  This
    # focused state decreases the ai's reaction time.  So it will know where it needs
    # to go but will be a little slower in getting there.  Once the ball is close enough
    # to the paddle, it will resume regular tracking.


    def __init__(self, min_react, max_react, h_zone_min, h_zone_max):
        self.frames_since_last_move = 0
        self.ai_min_react = min_react
        self.ai_max_react = max_react
        self.reaction_time = min_react
        self.hit_zone_min = h_zone_min
        self.hit_zone_max = h_zone_max
        self.hit_zone = self.hit_zone_min
        self.focused = False

    def set_reaction_time(self):
        # Sets a reaction time between ai_max_react and ai_min_react and
        # resets the frames counter.

        self.reaction_time = random.randint(self.ai_max_react, self.ai_min_react)
        self.frames_since_last_move = 0

    def _time_to_update_hit_zone(self):
        # We will update the AI's hit-zone randomly.
        return random.randint(self.hit_zone_min, self.hit_zone_max) == self.hit_zone

    def _update_hit_zone(self):
        # Set a new random hit-zone area.
        self.hit_zone = random.randint(self.hit_zone_min, self.hit_zone_max)

    def unfocus(self):
        # Turn off the focused state and get a new random reaction-time
        self.set_reaction_time()
        self.focused = False

    def focus(self, ball, paddle1, paddle2, elapsed):
        # Attempts to calculate the position the ball will hit 0 on the x-axis,
        # returns a fake ball that sits at that point.
        # reduce reaction time
        self.reaction_time *= 3
        if self.reaction_time > AI_REACT_CEILING:
            self.reaction_time = AI_REACT_CEILING
        self.focused = True
        # make a copy of the real ball in order to track its future movement
        ball_copy = ball.copy()
        screen_height = ball_copy._screen_info.height
        while (ball_copy.x_pos > PADDLE_GAP):
            while ball_copy.y_pos > 0 and ball_copy.y_pos < screen_height:
                ball_copy.x_pos += ball_copy.x_vel * (ball_copy.speed * elapsed)
                ball_copy.y_pos += ball_copy.y_vel * (ball_copy.speed * elapsed)
                if ball_copy.x_pos < 0:
                    break
            if ball_copy.y_pos <= 0 and ball_copy.x_pos > 0:
                ball_copy.y_pos = 1
            if ball_copy.y_pos >= screen_height and ball_copy.x_pos > 0:
                ball_copy.y_pos = screen_height - 1
            ball_copy.y_vel *= -1
        return ball_copy

    def update(self, paddle, ball):
        # This is where the AI will act.  If enough time has passed for the
        # AI to react, it will move its paddle's position to track the ball.
        # Otherwise, it will just increment the frame counter and wait.
        # The AI also has a 'hit-zone' which is the area of the paddle that
        # it will try to hit the ball with. This will vary randomly throughout
        # the game.

        if self.frames_since_last_move == self.reaction_time:
            if self._time_to_update_hit_zone():
                self._update_hit_zone()
            paddle_mid = paddle.y_pos + (paddle.height / 2)
            ball_mid = ball.y_pos + (ball.height / 2)
            # if the ball is below the paddles hit zone
            if ball.y_vel >= 0 and paddle_mid + self.hit_zone <= ball_mid:
                return 1
            # if the ball is above the paddles hit zone
            elif ball.y_vel <= 0 and paddle_mid - self.hit_zone >= ball_mid:
                return -1
            else:
                return 0
            self.frames_since_last_move = 0
        else:
            self.frames_since_last_move += 1
            return 0