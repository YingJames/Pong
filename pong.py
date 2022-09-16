import pygame

# constants
WIDTH, HEIGHT = 700, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PongAI")

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

class Paddle:
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if (up):
            self.y -= self.VEL
        else: 
            self.y += self.VEL

class Ball:
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, window):
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel


def draw(window, paddles, ball):
    window.fill(BLACK)

    for paddle in paddles:
        paddle.draw(window)

    # dashed line in the middle
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(window, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(WINDOW)
    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):

    # ball will bounce back at opposite direction touching top and bot of screen
    if (ball.y + ball.radius >= HEIGHT):
        ball.y_vel *= -1
    elif (ball.y - ball.radius <= 0):
        ball.y_vel *= -1

    # hitting the left paddle
    if (ball.x_vel < 0):
        if (ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height):
            if ((ball.x - ball.radius) <= (left_paddle.x + left_paddle.width)):
                ball.x_vel *= -1

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
                    ball.x_vel *= -1

                    middle_y = right_paddle.y + right_paddle.height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL 
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = y_vel * -1

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if (keys[pygame.K_w] and (left_paddle.y - left_paddle.VEL >= 0)):
        left_paddle.move(up=True)
    if (keys[pygame.K_s] and (left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT)):
        left_paddle.move(up=False)

    if (keys[pygame.K_UP] and (right_paddle.y - right_paddle.VEL >= 0)):
        right_paddle.move(up=True)
    if (keys[pygame.K_DOWN] and (right_paddle.y + right_paddle.VEL +right_paddle.height <= HEIGHT)):
        right_paddle.move(up=False)

def main():
    run = True
    clock = pygame.time.Clock()

    # draws paddle at the edges of the screen
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH //2, HEIGHT // 2, BALL_RADIUS)

    while run:
        # regulate game to 60fps
        clock.tick(FPS)
        
        draw(WINDOW, [left_paddle, right_paddle], ball) 

        for event in pygame.event.get():
            # when player clicks close window btn
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        handle_collision(ball, left_paddle, right_paddle)
        ball.move()

    pygame.quit()


if __name__ == '__main__':
    main()
