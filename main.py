import pygame
from pong.game import Game

class PongGame:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 700, 500
        self.pong = Game(self.WIDTH, self.HEIGHT)

    def execute(self):
        is_running = True

        while is_running:
            clock = pygame.time.Clock()
            clock.tick(60)
            game_info = self.pong.loop()
            
            for event in pygame.event.get():
                # when player clicks close window btn
                if event.type == pygame.QUIT:
                    is_running = False
                    break
        pygame.quit()

if __name__ == "__main__":
    pong_program = PongGame()
    pong_program.execute()