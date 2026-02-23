import pygame
from scene.base_scene import Scene
from entity.text_box import TextBox

class GameScene(Scene):
    """
    Main game scene class for the program.
    """

    def __init__(self, game):
        super().__init__(game)

        self.font = pygame.font.Font("Game/asset/font/NotoSans-Medium.ttf", 42)

        self.text_box = TextBox(
            font=self.font,
            size=(520, 70),
            text_color=(255, 255, 255),
            idle_color=(70, 70, 80),
            active_color=(110, 110, 130),
        )

    def manage_event(self, events):
        super().manage_event(events)

        for event in events:
            if event.type == pygame.QUIT:
                self.request_quit = True

            result = self.text_box.interact(event)
            if result == "enter":
                print("Typed:", self.text_box.text)

    def update(self):
        pass

    def draw(self, screen):
        # Reset screen
        screen.fill((10, 10, 15))

        # Define center guideline
        center_x = self.game.WIDTH // 2
        center_y = self.game.HEIGHT // 2

        # Text box
        self.text_box.center(center_x, center_y)
        self.text_box.draw(screen)