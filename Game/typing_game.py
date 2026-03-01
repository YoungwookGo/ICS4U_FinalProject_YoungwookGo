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
from scene.over_scene import OverScene

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

        self.clock = pygame.time.Clock() # Game clock
        self.running = True # Game loop state

        # Initialize game screen
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.FPS = 60
        pygame.display.set_caption("Typing Game")
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        # Initialize stats
        self.last_score = 0
        self.high_score = 0
        self.is_high_score = False

        # Initialize game scene
        self.scene = MenuScene(self)

    def run(self):
        """Main game loop"""

        while self.running:
            event = pygame.event.get()

            self.scene.manage_event(event)
            self.scene.update()
            self.scene.draw(self.screen)

            pygame.display.flip()
            self.manage_scene()

            self.clock.tick(self.FPS)

        # Quit game loop when loop ends
        self.quit()

    def manage_scene(self):
        """Switch scene if requested"""

        # Quit request
        if self.scene.request_quit:
            self.running = False
            return

        # Scene change request
        scene_key = self.scene.request_scene

        if scene_key is None:
            return

        if scene_key == "menu":
            self.scene = MenuScene(self)
        elif scene_key == "game":
            self.scene = GameScene(self)
        elif scene_key == "over":
            self.scene = OverScene(self)
        else:
            print("Invalid scene request: ", scene_key)

        self.scene.request_scene = None


    def quit(self):
        """Close the game"""

        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
