import pygame
from scene.base_scene import Scene
from utility.button import Button

class OverScene(Scene):
    """
    Gave Over scene.
    Displays statistics and button.
    """

    def __init__(self, game):
        super().__init__(game)

        # Fonts
        self.title_font = pygame.font.Font("Game/asset/font/NotoSans-SemiBold.ttf", 80)
        self.button_font = pygame.font.Font("Game/asset/font/NotoSans-SemiBold.ttf", 40)

        # Create title and button
        self.title_surface = self.title_font.render("Game Over!", True, (255, 255, 255))

        self.start_button = Button(
            font=self.button_font,
            text="START",
            size=(220, 70),
            text_color=(0, 0, 0),
            idle_color=(200, 200, 200),
            active_color=(255, 255, 255),
        )

        self.menu_button = Button(
            font=self.button_font,
            text="MENU",
            size=(220, 70),
            text_color=(0, 0, 0),
            idle_color=(200, 200, 200),
            active_color=(255, 255, 255),
        )

        self.stat_button = Button(
            font=self.button_font,
            text="STAT",
            size=(220, 70),
            text_color=(0, 0, 0),
            idle_color=(200, 200, 200),
            active_color=(255, 255, 255),
        )

    def manage_event(self, events):
        super().manage_event(events)

        for event in events:
            if self.start_button.interact(event):
                self.request_scene = "game"

            if self.menu_button.interact(event):
                self.request_scene = "menu"

    def update(self):
        pass

    def draw(self, screen):
        # Reset screen
        screen.fill((30, 30, 40))

        # Define center guideline
        center_x = self.game.WIDTH // 2
        center_y = self.game.HEIGHT // 2

        # Title 
        title_rect = self.title_surface.get_rect(center=(center_x, center_y - 100))
        screen.blit(self.title_surface, title_rect)

        # ----- Button -----
        self.start_button.locate(center_x - 120, center_y + 20)
        self.start_button.draw(screen)

        self.menu_button.locate(center_x + 120, center_y + 20)
        self.menu_button.draw(screen)

        self.stat_button.locate(center_x, center_y + 110)
        self.stat_button.draw(screen)