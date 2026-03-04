# #####################################
# Class Name:   Button
# Course:       ICS4U 
# Author:       Youngwook Go 
# Date:         2026-03-01
# File Name:    button.py 
# Description:  
#   This class manages the button user interface,
#   including active/idle effects, click handling, and drawing the button on the screen.
##############################################
import pygame

class Button:
    """
    Simple reusable button class
    - Have clickable rectangle
    - Detect interaction
    - Change color when moue hovers
    """
    # Constant for button box rounded corners
    BORDER_RADIUS = 8
    TEXT_Y_OFFSET = -2

    def __init__(self, font, text, size, text_color, idle_color, active_color):
        """
        Initialize the Button object.
        """
        self.font = font
        self.text = text

        # Color settings
        self.text_color = text_color
        self.idle_color = idle_color
        self.active_color = active_color

        # Rectangle defines the clickable area.
        self.rect = pygame.Rect(0, 0, size[0], size[1])

        # Pre-render the text surface for performance.
        self.__render_text()
    #end __init__()

    def __render_text(self):
        """
        Render the text surface.
        - If the text changes later, this method can re-render consistently.
        """
        self.text_surface = self.font.render(self.text, True, self.text_color)
    #end __render_text()

    def locate(self, x, y):
        """
        Set location of the button's center
        """
        self.rect.center = (x, y)
    #end locate()

    def interact(self, event):
        """
        Detect a left mouse click inside the button.
        """
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )
    #end interact()
    
    def draw(self, screen):
        """
        Draw the button and its centered text.
        """
        mouse_pos = pygame.mouse.get_pos()
        color = self.active_color if self.rect.collidepoint(mouse_pos) else self.idle_color

        pygame.draw.rect(screen, color, self.rect, border_radius=self.BORDER_RADIUS)

        # Re-center text every draw 
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        text_rect.centery += self.TEXT_Y_OFFSET
        screen.blit(self.text_surface, text_rect)
    #end draw()

class IconButton(Button):
    TEXT_Y_OFFSET = 6