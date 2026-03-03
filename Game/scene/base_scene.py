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

class Scene:
    """
    Base class for all scenes.
    Scenes should only request a scene change by setting request_scene.
    """
    GAME_SCENE = "game"
    MENU_SCENE = "menu"
    OVER_SCENE = "over"
    
    def __init__(self, game):
        """
        Initialize the base scene.
        """
        self.game = game

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