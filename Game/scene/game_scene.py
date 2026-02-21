import pygame
from scene.base_scene import Scene


class GameScene(Scene):
    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("arial", 28)

        self.p1 = (width // 2, height // 2 - 80)
        self.p2 = (width // 2 - 120, height // 2 + 80)
        self.p3 = (width // 2 + 120, height // 2 + 80)

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.QUIT:
                self.next_scene = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_scene = False

    def update(self):
        pass

    def draw(self, screen):

        screen.fill((0, 0, 0))

        text = self.font.render("This is Game Scene (ESC = Quit)", True, (255, 255, 255))
        screen.blit(text, (20, 20))