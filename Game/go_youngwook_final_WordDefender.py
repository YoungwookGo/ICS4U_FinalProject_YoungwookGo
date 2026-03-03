# #####################################
# Program Name: WordDefender
# Course:       ICS4U
# Author:       Youngwook Go
# Date:         2026-03-01
# File Name:    go_youngwook_final_WordDefender.py
# Description:
#   WordDefender is a real-time word typing challenge game.

#   Game Overview:
#   The player must type moving words correctly before they reach
#   the right side of the screen. Different enemy types have unique
#   behaviors such as increased speed, multiple health points, or
#   special rewards. The game increases in difficulty over time.

# Core Features:
#   - Real-time typing input system
#   - Multiple enemy types using inheritance
#   - Dynamic speed calculation based on word length
#   - Energy and health reward system
#   - Scene management (Menu, Game, Over)
#   - High score tracking and statistics saving

# Programming Concepts Demonstrated:
#   - OOP (Encapsulation, Inheritance, Polymorphism)
#   - Sprite-based movement system
#   - Scene/state management architecture
#   - Event-driven input handling
#   - File-based data persistence
# #####################################

# Python library for building 2D games
import pygame
import sys

# Import scenes
from scene.menu_scene import MenuScene
from scene.game_scene import GameScene
from scene.over_scene import OverScene

class Game:
    """
    Main class for typing game named Word Defender.
    Handle initialization, game loop,
    events, updating, and drawing.
    """

    # Initialize game screen
    WIDTH = 1280
    HEIGHT = 720
    FPS = 60
    GAME_NAME = "Word Defender"

    def __init__(self):
        """
        Initialize the game engine, window, and default state.
        """
        # Initialize pygame modules
        pygame.init()

        # Create clock for frame rate control
        self.clock = pygame.time.Clock()
        self.running = True

        # Create the main window
        pygame.display.set_caption(self.GAME_NAME)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        # Initialize stats
        self.last_score = 0
        self.high_score = 0
        self.is_high_score = False

        # Initialize game scene
        self.scene = MenuScene(self)
    #end __init__()

    def run(self):
        """
        Run main game loop
        """

        while self.running:
            # Get all events
            events = pygame.event.get()

            # Let the current scene handle input/events
            self.scene.manage_event(events)

            # Update scene logic
            self.scene.update()

            # Draw current scene
            self.scene.draw(self.screen)

            # Update the screen
            pygame.display.flip()

            # Switch scenes if requested
            self.manage_scene()

            # Maintain a stable FPS for consistent gameplay
            self.clock.tick(self.FPS)

        # Quit game loop when loop ends
        self.quit()
    #end run()

    def manage_scene(self):
        """
        Switch scenes if the current scene requests a change.
        """
        # Quit request
        if self.scene.request_quit:
            self.running = False
            return

        # Scene change request
        scene_key = self.scene.request_scene
        if scene_key is None:   # No change
            return

        # Replace current scene based on requested key
        if scene_key == "menu":
            self.scene = MenuScene(self)
        elif scene_key == "game":
            self.scene = GameScene(self)
        elif scene_key == "over":
            self.scene = OverScene(self)
        else:
            # Invalid request should not crash the program
            print(f"Game ERROR: Invalid scene request -> {scene_key}")

        # Reset request after switching to prevent repeated switching
        self.scene.request_scene = None
    #end manage_scene()

    def quit(self):
        """
        Close the game
        """
        pygame.quit() # Clean up pygame modules.
        sys.exit() # Stop the program execution.
    #end quit()

def main():
    """
    Entry point for the program.
    """
    game = Game()
    game.run()
#end main()

if __name__ == "__main__":
    main()
