import pygame
from scene.base_scene import Scene

class MenuScene(Scene):
    """
    Game menu scene class for the program.
    """

    def __init__(self, game):
        """Initialize menu scene"""

        super().__init__(game)

        self.font = pygame.font.SysFont(None, 48)

        self.start_button = pygame.Rect(412, 280, 200, 70)

    def manage_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.request_quit = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.start_button.collidepoint(event.pos):
                    self.request_scene = "game"

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        title = self.font.render("MENU: Click START", True, (255, 255, 255))
        screen.blit(title, (330, 150))

        pygame.draw.rect(screen, (80, 80, 80), self.start_button)
        text = self.font.render("START", True, (255, 255, 255))
        screen.blit(text, (self.start_button.x + 45, self.start_button.y + 15))