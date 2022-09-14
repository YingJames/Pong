import pygame

# constants
WIDTH, HEIGHT = 700, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PongAI")

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw(window):
    window.fill(BLACK)
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    
    while run:
        # regulate game to 60fps
        clock.tick(FPS)
        draw(WINDOW) 

        for event in pygame.event.get():

            # when player clicks close window btn
            if event.type == pygame.QUIT:
                run = False
                break

    pygame.quit()


if __name__ == '__main__':
    main()
