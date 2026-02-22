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

import sys
import pygame

# Import scene
from scene.menu_scene import MenuScene
from scene.game_scene import GameScene

class Game:
    """
    Main class for typing game.
    Handle initialization, game loop,
    events, updating, and drawing.
    """

    def __init__(self):
        """Initialize game"""

        # Initialize game engine
        pygame.init()

        self.clock = pygame.time.Clock() # Game clock for frame control
        self.running = True # Game loop state

        # Initialize game screen
        self.WIDTH = 1024
        self.HEIGHT = 640
        self.FPS = 60
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Typing Game")

        # Initialize game scene
        self._register_scene()
        self.scene = self.scene_registry["menu"]

    def run(self):
        """Main game loop"""

        while self.running:
            event = pygame.event.get()

            self.scene.manage_event(event)
            self.scene.update()
            self.scene.draw(self.screen)

            pygame.display.flip()
            self._manage_scene()

            self.clock.tick(60)

        # Quit game loop when loop ends
        self.quit()

    def _register_scene(self):
        """Register all scenes, only for initialize"""

        self.scene_registry = {}

        self.scene_registry["menu"] = MenuScene(self)
        self.scene_registry["game"] = GameScene(self)

    def _manage_scene(self):
        """Switch scene if requested"""

        # Quit request
        if self.scene.request_quit:
            self.running = False
            return

        # Scene change request
        scene_key = self.scene.request_scene

        if scene_key is None:
            return

        if scene_key in self.scene_registry:
            self.scene.request_scene = None
            self.scene = self.scene_registry[scene_key]

    def quit(self):
        """Close the game"""

        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()