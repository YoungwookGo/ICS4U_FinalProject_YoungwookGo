import pygame

class Scene:
    """
    Base class for all scenes.
    Scenes should only request a scene change by setting request_scene.
    Game class performs the actual switch.
    """

    def __init__(self, game):
        self.game = game
        self.request_scene = None
        self.request_quit = False

    def manage_event(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.request_quit = True

    def update(self):
        pass

    def draw(self, screen):
        pass