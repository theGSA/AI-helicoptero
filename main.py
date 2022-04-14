import pygame
from Ambiente import Ambiente

BRANCO = 255


def main():
    display = [1024, 700]
    pygame.init()
    screen = pygame.display.set_mode(display)

    pygame.display.flip()
    amb = Ambiente(screen)
    running = True
    clock = pygame.time.Clock()
    count = 0
    elapsed = 0
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BRANCO)
        amb.Update()
        count += 1
        if pygame.time.get_ticks() - elapsed >= 1000:
            elapsed = pygame.time.get_ticks()
            pygame.display.set_caption("FPS: "+str(count))
            count = 0
        clock.tick(160)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
