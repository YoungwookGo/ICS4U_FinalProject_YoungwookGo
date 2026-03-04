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
from scene.base_scene import Scene
from utility.button import Button

class OverScene(Scene):
    """
    Gave Over scene.
    Displays statistics and button.
    """
    def __init__(self, game):
        """
        Initialize the game-over screen resources and UI.
        """
        super().__init__(game)

        # Determine title text
        if self.game.is_high_score:
            title_text = "New High Score!" 
        else:
            title_text = "Game Over!"

        # Initialize text surfaces
        self.title_surface = self.title_font.render(title_text, True, self.TEXT_COLOR_LIGHT)

        self.high_score_surface = self.content_font.render(
            f"High Score: {self.game.high_score}", True, self.TEXT_COLOR_LIGHT
        )
        self.score_surface = self.content_font.render(
            f"Score: {self.game.last_score}", True, self.TEXT_COLOR_LIGHT
        )

        # Initialize buttons
        self.start_button = Button(
            font=self.button_font,
            text="START",
            size=self.BUTTON_SIZE,
            text_color=self.TEXT_COLOR_DARK,
            idle_color=self.BUTTON_COLOR_IDLE,
            active_color=self.BUTTON_COLOR_ACTIVE,
        )

        self.quit_button = Button(
            font=self.button_font,
            text="QUIT",
            size=self.BUTTON_SIZE,
            text_color=self.TEXT_COLOR_LIGHT,
            idle_color=self.QUIT_BUTTON_COLOR_IDLE,
            active_color=self.QUIT_BUTTON_COLOR_ACTIVE,
        )

        self.stat_button = Button(
            font=self.button_font,
            text="STAT",
            size=self.BUTTON_SIZE,
            text_color=self.TEXT_COLOR_DARK,
            idle_color=self.BUTTON_COLOR_IDLE,
            active_color=self.BUTTON_COLOR_ACTIVE,
        )

        # Place buttons
        self.start_button.locate(self.center_x - 120, self.center_y + 110)
        self.quit_button.locate(self.center_x + 120, self.center_y + 110)
        # self.stat_button.locate(self.center_x, self.center_y + 200) 
    #end __init__()

    def manage_event(self, events):
        """
        Handle game-over input events.
        """
        super().manage_event(events)

        for event in events:
            # Button events
            if self.start_button.interact(event):
                self.request_scene = self.GAME_SCENE

            if self.quit_button.interact(event):
                self.request_quit = True
    #end manage_event()

    def update(self):
        pass
    #end update()

    def draw(self, screen):
        """
        Draw title, score summary, and menu buttons.
        """
        # Reset screen
        screen.fill(self.BACKGROUND_COLOR)

        # Draw texts
        title_rect = self.title_surface.get_rect(
            center=(self.center_x, self.center_y - 100)
        )
        score_rect = self.score_surface.get_rect(
            center=(self.center_x, self.center_y - 20)
        )
        high_score_rect = self.high_score_surface.get_rect(
            center=(self.center_x, self.center_y + 25)
        )

        screen.blit(self.title_surface, title_rect)
        screen.blit(self.score_surface, score_rect)
        screen.blit(self.high_score_surface, high_score_rect)

        # Draw buttons
        self.start_button.draw(screen)
        self.quit_button.draw(screen)

    #end draw()
#end class OverScene
