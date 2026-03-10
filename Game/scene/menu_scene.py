# #####################################
# Class Name:   MenuScene
# Course:       ICS4U 
# Author:       Youngwook Go 
# Date:         2026-03-05
# File Name:    menu_scene.py
# Description:  
#   MenuScene class is child class of Scene to handle the main menu screen.
#    - Display the game title and menu buttons.
#    - Allow the player to start the game or quit safely.
#    - Demonstrate clean scene separation using OOP inheritance.
# #####################################
from scene.base_scene import Scene
from utility.overlay_menu import OverlayMenuManager, GuideOverlayMenu

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
            self._status_gameover()
        else:
            self._status_neutral()
        # Initialize text surfaces
        self.title_surface = self.title_font.render(self.title_text, True, self.TEXT_COLOR_LIGHT)

        # Initialize buttons
        self.quit_button.locate(self.center_x - 240, self.center_y + 110)
        self.guide_button.locate(self.center_x, self.center_y + 110)
        self.start_button.locate(self.center_x + 240, self.center_y + 110)

        # Initialize overlay menus
        self.overlay_menu = OverlayMenuManager(self.game, self)
        self.overlay_menu.register("guide", GuideOverlayMenu(self.game, self))
    #end __init__()

    def _status_neutral(self):
        """
        Set title text for neutral menu
        """
        self.title_text = "Word Defender"
    #end _status_neutral()

    def _status_gameover(self):
        """
        Set the title text for the Game Over screen.

        If the player's score is a new high score, the title will display
        "New High Score!". Otherwise, it will display "Game Over!".
        """

        # Check whether the current score is a new high score
        if self.game.is_high_score:
            self.title_text = "New High Score!" 
        else:
            self.title_text = "Game Over!"

        # Print score and high score for game over menu
        self.high_score_surface = self.content_font.render(
            f"High Score: {self.game.high_score}", True, self.TEXT_COLOR_LIGHT
        )
        self.score_surface = self.content_font.render(
            f"Your Score: {self.game.last_score}", True, self.TEXT_COLOR_LIGHT
        )
    #end _status_gameover()

    def manage_event(self, events):
        """
        Handle menu input events.
        """
        super().manage_event(events)

        for event in events:
            # When an overlay is open, handle only overlay events.
            if self.overlay_menu.is_open():
                action = self.overlay_menu.handle_event(event)
                self._manage_overlay_event(action)
                continue

            # GUIDE button opens guide overlay.
            if self.guide_button.interact(event):
                self.overlay_menu.open("guide")
                continue

            # START button requests the game scene.
            if self.start_button.interact(event):
                self.request_scene = self.GAME_SCENE

            # QUIT button requests safe game exit.
            if self.quit_button.interact(event):
                self.request_quit = True
    #end manage_event()

    def _manage_overlay_event(self, action):
        """
        Handle action returned from the currently active overlay menu.
        """
        if action == "back":
            self.overlay_menu.close()
    #end _manage_overlay_event()

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

        # Draw overlay on top if opened.
        self.overlay_menu.draw(screen)
    #end draw()

    def _draw_gameover(self, screen):
        """
        Draw the score information on the Game Over screen.

        This function displays the player's current score and the
        highest score at the center of the screen.
        """

        # Create a rectangle for the current score text
        # Position it slightly above the center of the screen
        score_rect = self.score_surface.get_rect(
            center=(self.center_x, self.center_y - 20)
        )

        # Create a rectangle for the high score text
        # Position it slightly below the center of the screen
        high_score_rect = self.high_score_surface.get_rect(
            center=(self.center_x, self.center_y + 25)
        )

        # Draw the score and high score text onto the screen
        screen.blit(self.score_surface, score_rect)
        screen.blit(self.high_score_surface, high_score_rect)
    #end _draw_gameover()
#end class MenuScene
