# #####################################
# Program Name: Typing Practice Game
# Course:       ICS4U
# Author:       Youngwook Go
# Date:         2026-02-
# File Name:    typing_game.py
# Description:
#   The typing game program using
#   object-oriented structure in 
#   Pygame community edition.
# #####################################

import pygame
import sys
from scene.menu_scene import MenuScene

class Game:
    """
    Main class for typing game.
    Handle initialization, game loop,
    events, updating, and drawing.
    """

    def __init__(self):
        """Initialize game and setting"""

        # Initialize game engine
        pygame.init()

        # Initialize game screen
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Typing Game")

        self.clock = pygame.time.Clock() # Game clock for frame control

        self.running = True # Game state

        self.scene = MenuScene(self.WIDTH, self.HEIGHT) # Initial scene

    def run(self):

        while self.running:

            events = pygame.event.get()

            self.scene.handle_events(events)
            self.scene.update()
            self.scene.draw(self.screen)

            pygame.display.flip()

            self.change_scene_conditional()

            self.clock.tick(60)

        # Quit game loop when loop ends
        self.quit()

    def change_scene_conditional(self):
        if self.scene.next_scene is None:
            return

        if self.scene.next_scene is False:
            self.running = False
            return

        self.scene = self.scene.next_scene

    def quit(self):
        """Close the game"""
        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()