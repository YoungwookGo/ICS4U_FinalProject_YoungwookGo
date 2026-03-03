# #####################################
# Class Name:   OverScene
# Course:       ICS4U 
# Author:       Youngwook Go 
# Date:         2026-03-02
# File Name:    over_scene.py
# Description:  
#   OverScene class handles the game-over screen.
#    - Display the player's last score and the saved high score.
#    - Provide clear navigation buttons (Restart / Menu).
#    - Keep scene transitions controlled by request flags.
# #####################################
import pygame
from scene.base_scene import Scene
from utility.button import Button

class OverScene(Scene):
    """
    Gave Over scene.
    Displays statistics and button.
    """
    # Visual constants
    BG_COLOR = (30, 30, 40)
    TEXT_COLOR = (255, 255, 255) # white
    IDLE_COLOR = (200, 200, 200) # Light Gray
    BLACK_COLOR = (0, 0, 0)

    # Layout constants
    TITLE_OFFSET_Y = -100
    SCORE_OFFSET_Y = -20
    HIGH_SCORE_OFFSET_Y = 25
    BUTTON_OFFSET_Y = 110
    BUTTON_GAP_X = 120
    BUTTON_OFFSET_STAT = 200

    # Font settings
    FONT_PATH = "Game/asset/font/NotoSans-SemiBold.ttf"
    TITLE_FONT_SIZE = 80
    SCORE_FONT_SIZE = 36
    BUTTON_FONT_SIZE = 40

    # Button settings
    BUTTON_SIZE = (220, 70)

    def __init__(self, game):
        """
        Initialize the game-over screen resources and UI.
        """
        super().__init__(game)

        # Fonts
        self.title_font = pygame.font.Font(self.FONT_PATH, self.TITLE_FONT_SIZE)
        self.score_font = pygame.font.Font(self.FONT_PATH, self.SCORE_FONT_SIZE)
        self.button_font = pygame.font.Font(self.FONT_PATH, self.BUTTON_FONT_SIZE)

        # Define center guideline
        self.center_x = self.game.WIDTH // 2
        self.center_y = self.game.HEIGHT // 2

        # Title text depends on whether a new high score was achieved
        if self.game.is_high_score:
            title_text = "New High Score!" 
        else:
            title_text = "Game Over!"
        self.title_surface = self.title_font.render(title_text, True, self.TEXT_COLOR)

        # Score text surfaces
        self.high_score_surface = self.score_font.render(
            f"High Score: {self.game.high_score}", True, self.TEXT_COLOR
        )
        self.score_surface = self.score_font.render(
            f"Score: {self.game.last_score}", True, self.TEXT_COLOR
        )

        # Buttons
        self.start_button = Button(
            font=self.button_font,
            text="START",
            size=self.BUTTON_SIZE,
            text_color=self.BLACK_COLOR,
            idle_color=self.IDLE_COLOR,
            active_color=self.TEXT_COLOR,
        )

        self.menu_button = Button(
            font=self.button_font,
            text="MENU",
            size=self.BUTTON_SIZE,
            text_color=self.BLACK_COLOR,
            idle_color=self.IDLE_COLOR,
            active_color=self.TEXT_COLOR,
        )

        self.stat_button = Button(
            font=self.button_font,
            text="STAT",
            size=self.BUTTON_SIZE,
            text_color=(0, 0, 0),
            idle_color=self.IDLE_COLOR,
            active_color=self.TEXT_COLOR,
        )

        # Place buttons once
        self.start_button.locate(self.center_x - self.BUTTON_GAP_X, self.center_y + self.BUTTON_OFFSET_Y)
        self.menu_button.locate(self.center_x + self.BUTTON_GAP_X, self.center_y + self.BUTTON_OFFSET_Y)
        # self.stat_button.locate(self.center_x, self.center_y + self.BUTTON_OFFSET_STAT)
    #end __init__()

    def manage_event(self, events):
        """
        Handle game-over input events.
        """
        super().manage_event(events)

        for event in events:
            if self.start_button.interact(event):
                self.request_scene = self.GAME_SCENE

            if self.menu_button.interact(event):
                self.request_scene = self.MENU_SCENE
    #end manage_event()

    def update(self):
        pass
    #end update()

    def draw(self, screen):
        """
        Draw title, score summary, and menu buttons.
        """
        # Reset screen
        screen.fill(self.BG_COLOR)

        # Title 
        title_rect = self.title_surface.get_rect(
            center=(self.center_x, self.center_y + self.TITLE_OFFSET_Y)
        )
        screen.blit(self.title_surface, title_rect)

        # Scores
        score_rect = self.score_surface.get_rect(
            center=(self.center_x, self.center_y + self.SCORE_OFFSET_Y)
        )
        high_score_rect = self.high_score_surface.get_rect(
            center=(self.center_x, self.center_y + self.HIGH_SCORE_OFFSET_Y)
        )

        screen.blit(self.score_surface, score_rect)
        screen.blit(self.high_score_surface, high_score_rect)

        # Buttons
        self.start_button.draw(screen)
        self.menu_button.draw(screen)
        # self.stat_button.draw(screen)
    #end draw()
#end class OverScene