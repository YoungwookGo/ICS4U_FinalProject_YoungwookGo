import pygame
from scene.base_scene import Scene
from entities.button import Button

class MenuScene(Scene):
    """
    Main Menu Scene.
    Displays title and button.
    """

    def __init__(self, game):
        super().__init__(game)

        # Fonts
        self.title_font = pygame.font.Font("Game/asset/font/NotoSans-SemiBold.ttf", 80)
        self.button_font = pygame.font.Font("Game/asset/font/NotoSans-SemiBold.ttf", 40)

        # Create title and button
        self.title_surface = self.title_font.render("Typing Game", True, (255, 255, 255))
        
        self.start_button = Button(
            font=self.button_font,
            text="START",
            size=(220, 70),
            text_color=(0, 0, 0),
            idle_color=(200, 200, 200),
            hover_color=(255, 255, 255),
        )

        self.quit_button = Button(
            font=self.button_font,
            text="QUIT",
            size=(220, 70),
            text_color=(255, 255, 255),
            idle_color=(170, 50, 50),
            hover_color=(220, 70, 70),
        )


    def manage_event(self, events):
        super().manage_event(events)

        for event in events:
            if event.type == pygame.QUIT:
                self.request_quit = True

            if self.start_button.interact(event):
                self.request_scene = "game"

            if self.quit_button.interact(event):
                self.request_quit = True

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
        self.start_button.center(center_x, center_y + 20)
        self.start_button.draw(screen)

        self.quit_button.center(center_x, center_y + 110)
        self.quit_button.draw(screen)