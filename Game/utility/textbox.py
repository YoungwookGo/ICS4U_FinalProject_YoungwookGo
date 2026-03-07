# #####################################
# Class Name:   TextBox
# Course:       ICS4U 
# Author:       Youngwook Go 
# Date:         2026-03-01
# File Name:    textbox.py 
# Description:  
#   This class handles text input actions.
#    - Create an input box that can be reused across scenes (Menu, Game, Over).
#    - Support mouse activation, keyboard typing, backspace deletion, and Enter submission.
#    - Display a blinking cursor to notice typing area.
##############################################
import pygame

class TextBox:
    """
    TextBox is a reusable UI component for typing input.
    - Click to activate
    - Type to input
    - Backspace to delete
    """

    # Default UI constants
    DEFAULT_PADDING_X = 12
    CURSOR_THICKNESS = 3
    CURSOR_GAP = 3
    CURSOR_INTERVAL = 0.5  # seconds
    PLACEHOLDER_TEXT = "click and type here"
    PLACEHOLDER_COLOR = (140, 140, 140)

    def __init__(self, font, size, text_color, idle_color, active_color, max_length=30):
        """
        Initialize the TextBox object.
        """
        self.font = font
        self.text = ""

        # Visual settings
        self.text_color = text_color
        self.idle_color = idle_color
        self.active_color = active_color

        # Input behavior settings
        self.max_length = max_length

        # Rectangle that defines the position and size of the text box
        self.rect = pygame.Rect(0, 0, size[0], size[1])
        # Active means the box accepts keyboard input.
        self.active = True

        # Cursor blinking settings.
        self.cursor_timer = 0.0
        self.cursor_interval = self.CURSOR_INTERVAL
        self.cursor_visible = True
    #end __init__()

    def locate(self, x, y):
        """
        Set the location of the text box using its center position.
        """
        self.rect.center = (x, y)
    #end locate()

    def clear(self):
        """
        Clear all typed text.
        """
        self.text = ""
    #end clear()

    def get_text(self):
        """
        Return the current typed text.
        """
        return self.text
    #end get_text()

    def update(self, dt):
        """
        Update cursor blinking using delta time (dt).
        """
        if not self.active:
            return

        self.cursor_timer += dt

        # Toggle the cursor visibility at a fixed interval.
        if self.cursor_timer >= self.cursor_interval:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible
    #end update()

    def interact(self, event):
        """
        Re-activates when user click.
        """
        # Activate only when user clicks inside the box.
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)

        # Ignore key input when inactive.
        if not self.active:
            return None

        # Handle key input
        if event.type == pygame.KEYDOWN:
            # Backspace deletes last character
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                return None
            
            # Submit input
            if event.key == pygame.K_RETURN:
                return "enter"

            # event.unicode contains the typed character
            typed_char = event.unicode
            # Add typed character if it is alphabet and under max_length.
            if ('a' <= typed_char <= 'z') or ('A' <= typed_char <= 'Z'):
                if len(self.text) < self.max_length:
                    self.text += typed_char

        return None
    #end interact()
    
    def draw(self, screen):
        """
        Draw the text box, the typed text, and the blinking cursor.
        """
        # Select box color based on active state
        color = self.active_color if self.active else self.idle_color
        # Draw the text box background.
        pygame.draw.rect(screen, color, self.rect, border_radius=8)

        # Horizontal padding for text
        padding_x = self.DEFAULT_PADDING_X

        # Always draw actual typed text first.
        text_surface = self.font.render(self.text, True, self.text_color)
        
        # Center text vertically inside the box
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (self.rect.x + padding_x, text_y))

        # When text is empty, draw placeholder as an overlay.
        if self.text == "":
            placeholder_surface = self.font.render(
                self.PLACEHOLDER_TEXT, True, self.PLACEHOLDER_COLOR
            )
            screen.blit(placeholder_surface, (self.rect.x + padding_x, text_y))

        # Draw cursor after the text.
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + padding_x + text_surface.get_width() + self.CURSOR_GAP
            cursor_y = text_y + 5
            cursor_height = text_surface.get_height() - 10

            pygame.draw.line(
                screen,
                self.text_color,
                (cursor_x, cursor_y),
                (cursor_x, cursor_y + cursor_height),
                self.CURSOR_THICKNESS
            )
    #end draw()
