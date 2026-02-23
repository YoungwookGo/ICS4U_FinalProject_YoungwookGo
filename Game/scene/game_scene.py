import pygame
from scene.base_scene import Scene

class GameScene(Scene):
    """
    Main game scene class for the program.
    """

    def __init__(self, game):
        super().__init__(game)

    def manage_event(self, events):
        super().manage_event(events)

        for event in events:
            if event.type == pygame.QUIT:
                self.request_quit = True

    def update(self):
        pass

    def draw(self, screen):
        pass