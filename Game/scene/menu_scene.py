# #####################################
# Class Name:   MenuScene
# Course:       ICS4U 
# Author:       Youngwook Go 
# Date:         2026-03-02
# File Name:    menu_scene.py
# Description:  
#   MenuScene class is child class of Scene to handle the main menu screen.
#    - Display the game title and menu buttons.
#    - Allow the player to start the game or quit safely.
#    - Demonstrate clean scene separation using OOP inheritance.
# #####################################
import pygame
from scene.base_scene import Scene
from utility.button import Button

class MenuScene(Scene):
    """
    Main Menu scene.
    Displays title and button.
    """

    # UI constants
    BG_COLOR = (30, 30, 40)
    TITLE_COLOR = (255, 255, 255)

    TITLE_TEXT = "Word Defender"

    TITLE_SIZE = 80
    BUTTON_TEXT_SIZE = 40
    BUTTON_SIZE = (220, 70)

    TITLE_OFFSET_Y = -100
    START_BUTTON_OFFSET_Y = 20
    QUIT_BUTTON_OFFSET_Y = 110

    FONT_PATH = "Game/asset/font/NotoSans-SemiBold.ttf"

    def __init__(self, game):
        """
        Initialize the menu scene.
        """
        super().__init__(game)

        # Fonts used in this scene
        self.title_font = pygame.font.Font(self.FONT_PATH, self.TITLE_SIZE)
        self.button_font = pygame.font.Font(self.FONT_PATH, self.BUTTON_TEXT_SIZE)

        # Create title and button
        self.title_surface = self.title_font.render(self.TITLE_TEXT, True, self.TITLE_COLOR)

        # Create buttons
        self.start_button = Button(
            font=self.button_font,
            text="START",
            size=self.BUTTON_SIZE,
            text_color=(0, 0, 0),
            idle_color=(200, 200, 200),
            active_color=(255, 255, 255),
        )

        self.quit_button = Button(
            font=self.button_font,
            text="QUIT",
            size=self.BUTTON_SIZE,
            text_color=(255, 255, 255),
            idle_color=(170, 50, 50),
            active_color=(220, 70, 70),
        )

        # Define center guideline
        self.center_x = self.game.WIDTH // 2
        self.center_y = self.game.HEIGHT // 2

        # Place buttons once
        self.start_button.locate(self.center_x, self.center_y + self.START_BUTTON_OFFSET_Y)
        self.quit_button.locate(self.center_x, self.center_y + self.QUIT_BUTTON_OFFSET_Y)
    #end __init__()

    def manage_event(self, events):
        """
        Handle menu input events.
        """
        super().manage_event(events)

        for event in events:
            # START button requests the game scene.
            if self.start_button.interact(event):
                self.request_scene = self.GAME_SCENE

            # QUIT button requests safe game exit.
            if self.quit_button.interact(event):
                self.request_quit = True
    #end manage_event()

    def update(self):
        """
        Update menu logic.
        """
        pass
    #end update()

    def draw(self, screen):
        """
        Draw the menu UI (background, title, and buttons).
        """
        # Reset screen
        screen.fill(self.BG_COLOR)

        # Draw title 
        title_rect = self.title_surface.get_rect(
            center=(self.center_x, self.center_y + self.TITLE_OFFSET_Y)
        )
        screen.blit(self.title_surface, title_rect)

        # Draw button
        self.start_button.draw(screen)
        self.quit_button.draw(screen)
    #end draw()
#end class MenuScene