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
from scene.base_scene import Scene
from utility.button import Button

class MenuScene(Scene):
    """
    Main Menu scene.
    Displays title and button.
    """
    def __init__(self, game, status = ""):
        """
        Initialize the menu scene.
        """
        super().__init__(game)

        # Change menu page by scene status
        self.status = status

        if self.status == "GAMEOVER":
            self._status_GAMEOVER()
        else:
            self._status_neutral()
        # Initialize text surfaces
        self.title_surface = self.title_font.render(self.title_text, True, self.TEXT_COLOR_LIGHT)

        # Initialize buttons
        self.quit_button.locate(self.center_x - 240, self.center_y + 110)
        self.guide_button.locate(self.center_x, self.center_y + 110)
        self.start_button.locate(self.center_x + 240, self.center_y + 110)
    #end __init__()

    def _status_neutral(self):
        # Title text for neutral menu
        self.title_text = "Word Defender"

    def _status_GAMEOVER(self):
        # Determine title text for game over menu
        if self.game.is_high_score:
            self.title_text = "New High Score!" 
        else:
            self.title_text = "Game Over!"

        # Print score and high schore for game over menu
        self.high_score_surface = self.content_font.render(
            f"High Score: {self.game.high_score}", True, self.TEXT_COLOR_LIGHT
        )
        self.score_surface = self.content_font.render(
            f"Your Score: {self.game.last_score}", True, self.TEXT_COLOR_LIGHT
        )

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
        screen.fill(self.BACKGROUND_COLOR)

        # Draw texts 
        menu_title_rect = self.title_surface.get_rect(
            center=(self.center_x, self.center_y -100)
        )
        screen.blit(self.title_surface, menu_title_rect)

        # Draw buttons
        self.quit_button.draw(screen)
        self.guide_button.draw(screen)
        self.start_button.draw(screen)

        if self.status == "GAMEOVER":
            self._draw_gameover(screen)
    #end draw()

    def _draw_gameover(self, screen):
        # Draw additional texts
        score_rect = self.score_surface.get_rect(
            center=(self.center_x, self.center_y - 20)
        )
        high_score_rect = self.high_score_surface.get_rect(
            center=(self.center_x, self.center_y + 25)
        )

        screen.blit(self.score_surface, score_rect)
        screen.blit(self.high_score_surface, high_score_rect)
#end class MenuScene