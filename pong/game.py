import pygame
from .ball import Ball
from .paddle import Paddle
pygame.init() 

class Game:

    def __init__(self, WIDTH, HEIGHT) -> None:
        pygame.display.set_caption("PongAI")

        # constants
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
        self.FPS = 60
        self.SCORE_FONT = pygame.font.SysFont("futura", 50)
        self.WINNING_SCORE = 5
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        
        # initial game set
        self.left_paddle = Paddle(10, self.HEIGHT//2 - Paddle.HEIGHT//2, Paddle.WIDTH, Paddle.HEIGHT)
        self.right_paddle = Paddle(self.WIDTH - 10 - Paddle.WIDTH, self.HEIGHT//2 - Paddle.HEIGHT//2, Paddle.WIDTH, Paddle.HEIGHT)
        self.ball = Ball(self.WIDTH //2, self.HEIGHT // 2, Ball.RADIUS)

        self.left_score = 0
        self.right_score = 0

    def render(self, window, paddles, ball, left_score, right_score):
        window.fill(self.BLACK)

        left_score_text = self.SCORE_FONT.render(f"{self.left_score}", 1, self.WHITE)
        right_score_text = self.SCORE_FONT.render(f"{self.right_score}", 1, self.WHITE)
        window.blit(left_score_text, (self.WIDTH // 4 - left_score_text.get_width()//2, 20))
        window.blit(right_score_text, (self.WIDTH * (3/4) - right_score_text.get_width()//2, 20))

        for paddle in paddles:
            paddle.draw(window)

        # dashed line in the middle
        for i in range(10, self.HEIGHT, self.HEIGHT//20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(window, self.WHITE, (self.WIDTH//2 - 5, i, 10, self.HEIGHT//20))

        ball.draw(self.WINDOW)
        pygame.display.update()

    def handle_collision(self, ball, left_paddle, right_paddle):

        # ball will bounce back at opposite direction touching top and bot of screen
        if (ball.y + ball.radius >= self.HEIGHT):
            ball.y_vel *= -1
        elif (ball.y - ball.radius <= 0):
            ball.y_vel *= -1

        # hitting the left paddle
        if (ball.x_vel < 0):
            if (ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height):
                if ((ball.x - ball.radius) <= (left_paddle.x + left_paddle.width)):
                    ball.x_vel = ball.flip(ball.x_vel)

                    # change y_vel based on where the ball hits the paddle
                    middle_y = left_paddle.y + left_paddle.height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL 
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = y_vel * -1

        else:
        # hitting the right paddle
            if (ball.x_vel > 0):
                if (ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height):
                    if ((ball.x + ball.radius) >= right_paddle.x):
                        ball.x_vel = ball.flip(ball.x_vel)

                        middle_y = right_paddle.y + right_paddle.height / 2
                        difference_in_y = middle_y - ball.y
                        reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL 
                        y_vel = difference_in_y / reduction_factor
                        ball.y_vel = y_vel * -1


    def handle_paddle_movement(self, keys, left_paddle, right_paddle):
        if (keys[pygame.K_w] and (left_paddle.y - left_paddle.VEL >= 0)):
            left_paddle.move(up=True)
        if (keys[pygame.K_s] and (left_paddle.y + left_paddle.VEL + left_paddle.height <= self.HEIGHT)):
            left_paddle.move(up=False)

        if (keys[pygame.K_UP] and (right_paddle.y - right_paddle.VEL >= 0)):
            right_paddle.move(up=True)
        if (keys[pygame.K_DOWN] and (right_paddle.y + right_paddle.VEL +right_paddle.height <= self.HEIGHT)):
            right_paddle.move(up=False)

    def handle_quitting(self):
        for event in pygame.event.get():
            # when player clicks close window btn
            if event.type == pygame.QUIT:
                pygame.quit()
                break


    def handle_scoring(self):
        if (self.ball.x < 0):
            self.right_score += 1
            self.ball.reset(self.ball.x)
        elif (self.ball.x > self.WIDTH):
            self.left_score += 1
            self.ball.reset(self.ball.x)

        won = False
        if (self.left_score >= self.WINNING_SCORE):
            won = True
            win_text = "Left Player Won!"

        elif (self.right_score >= self.WINNING_SCORE):
            won = True
            win_text = "Right Player Won!"

        if won:
            text = self.SCORE_FONT.render(win_text, 1, self.WHITE)
            self.WINDOW.blit(text, (self.WIDTH//2 - text.get_width()//2, self.HEIGHT//2 - text.get_height()//2))
            self.reset_game()

    def reset_game(self):
        pygame.display.update()
        pygame.time.delay(5000)
        self.ball.reset(0)
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.left_score = 0
        self.right_score = 0

    def loop(self): 
        self.render(self.WINDOW, [self.left_paddle, self.right_paddle], self.ball, self.left_score, self.right_score) 

        # reads key input
        keys = pygame.key.get_pressed()
        self.handle_paddle_movement(keys, self.left_paddle, self.right_paddle)

        # handle logic
        self.handle_quitting()
        self.ball.move()
        self.handle_collision(self.ball, self.left_paddle, self.right_paddle)
        self.handle_scoring()

