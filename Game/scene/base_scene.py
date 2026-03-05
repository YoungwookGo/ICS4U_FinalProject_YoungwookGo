# #####################################
# Class Name:   Scene
# Course:       ICS4U 
# Author:       Youngwook Go 
# Date:         2026-03-02
# File Name:    base_scene.py
# Description:  
#    Scene is the base class for all scenes (MenuScene, GameScene, OverScene).
#    - Provide a consistent interface for event handling, updating, and drawing.
#    - Allow scenes to request transitions without directly creating new scenes.
#    - Centralize common quit handling (window close button).
##############################################
import pygame
import os
from utility.button import Button 

class Scene:
    """
    Base class for all scenes.
    Scenes should only request a scene change by setting request_scene.
    """
    GAME_SCENE = "game"
    MENU_SCENE = "menu"
    OVER_SCENE = "over"

    # Shared file paths
    FONT_PATH_MEDIUM = os.path.join("Game", "asset", "font", "NotoSans-Medium.ttf")
    FONT_PATH_BOLD = os.path.join("Game", "asset", "font", "NotoSans-SemiBold.ttf")
    FONT_PATH_SYMBOL = os.path.join("Game", "asset", "font", "NotoSansSymbols2-Regular.ttf")
    WALLPAPER_DIR = os.path.join("Game", "asset", "wallpaper")

    # Shared visual constants
    BACKGROUND_COLOR = "#1E1E28"

    TEXT_COLOR_LIGHT = "#FFFFFF"
    TEXT_COLOR_DARK = "#000000"
    TEXT_COLOR_RED = "#FF3232"
    TEXT_COLOR_YELLOW = "#FFFF00"
    TEXT_COLOR_CYAN = "#00FFFF"

    BUTTON_COLOR_IDLE = "#C8C8C8"
    BUTTON_COLOR_ACTIVE = "#FFFFFF"

    START_BUTTON_COLOR_IDLE = "#32AA32"
    START_BUTTON_COLOR_ACTIVE = "#46DC46"

    QUIT_BUTTON_COLOR_IDLE = "#AA3232"
    QUIT_BUTTON_COLOR_ACTIVE = "#DC4646"

    PAUSE_MENU_COLOR = "#C8C8C8"

    TITLE_FONT_SIZE = 80
    CONTENT_FONT_SIZE = 32
    ICON_FONT_SIZE = 48

    TEXTBOX_FONT_SIZE = 48
    TEXTBOX_SIZE = (1000, 80)

    BUTTON_FONT_SIZE = 36
    BUTTON_SIZE = (220, 70)
    
    def __init__(self, game):
        """
        Initialize the base scene.
        """
        self.game = game

        # Define center guideline
        self.center_x = self.game.WIDTH // 2
        self.center_y = self.game.HEIGHT // 2

        # Shared font styles
        self.title_font = pygame.font.Font(self.FONT_PATH_BOLD, self.TITLE_FONT_SIZE)
        self.content_font = pygame.font.Font(self.FONT_PATH_BOLD, self.CONTENT_FONT_SIZE)
        self.button_font = pygame.font.Font(self.FONT_PATH_BOLD, self.BUTTON_FONT_SIZE)
        self.icon_font = pygame.font.Font(self.FONT_PATH_SYMBOL, self.ICON_FONT_SIZE)
        self.inputbox_font = pygame.font.Font(self.FONT_PATH_MEDIUM, self.TEXTBOX_FONT_SIZE)

        # Shared button
        self.quit_button = Button(
            font=self.button_font,
            text="Quit",
            size=self.BUTTON_SIZE,
            text_color=self.TEXT_COLOR_LIGHT,
            idle_color=self.QUIT_BUTTON_COLOR_IDLE,
            active_color=self.QUIT_BUTTON_COLOR_ACTIVE,
        )

        self.start_button = Button(
            font=self.button_font,
            text="Start",
            size=self.BUTTON_SIZE,
            text_color=self.TEXT_COLOR_DARK,
            idle_color=self.START_BUTTON_COLOR_IDLE,
            active_color=self.START_BUTTON_COLOR_ACTIVE,
        )

        self.guide_button = Button(
            font=self.button_font,
            text="Guide",
            size=self.BUTTON_SIZE,
            text_color=self.TEXT_COLOR_DARK,
            idle_color=self.BUTTON_COLOR_IDLE,
            active_color=self.BUTTON_COLOR_ACTIVE,
        )

        # Scene requests
        self.request_scene = None
        self.request_quit = False
    #end __init__()

    def manage_event(self, events):
        """
        Handle incoming pygame events.

        Default behavior:
        - Detect pygame.QUIT (window close) and request game shutdown.
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.request_quit = True
    #end manage_event()

    def update(self):
        """
        Update scene logic.
        """
        pass
    #end update()

    def draw(self, screen):
        """
        Draw the scene.
        Subclasses override this method to render UI and game objects.
        """
        pass
    #end draw()
#end class Scene
