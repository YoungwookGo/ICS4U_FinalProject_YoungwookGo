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
    def __init__(self, game):
        """
        Initialize the menu scene.
        """
        super().__init__(game)

        # Title text
        self.title_text = "Word Defender"

        # Initialize text surfaces
        self.title_surface = self.title_font.render(self.title_text, True, self.TEXT_COLOR_LIGHT)

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

        self.start_button.locate(self.center_x, self.center_y + 20)
        self.quit_button.locate(self.center_x, self.center_y + 110)
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
        screen.fill(self.BACKGROUND_COLOR)

        # Draw texts 
        title_rect = self.title_surface.get_rect(
            center=(self.center_x, self.center_y -100)
        )
        screen.blit(self.title_surface, title_rect)

        # Draw buttons
        self.start_button.draw(screen)
        self.quit_button.draw(screen)
    #end draw()
#end class MenuScene