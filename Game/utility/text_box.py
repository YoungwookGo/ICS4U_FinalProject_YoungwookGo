import pygame

class TextBox:
    """
    Simple reusable text box class
    - Click to activate
    - Type to input
    - Backspace to delete
    """

    def __init__(self, font, size, text_color, idle_color, active_color):
        self.font = font
        self.text = ""

        self.text_color = text_color
        self.idle_color = idle_color
        self.active_color = active_color

        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.active = True

    def locate(self, x, y):
        # Set location of the text box's center
        self.rect.center = (x, y)

    def interact(self, event):

        # Re-activates when user click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)

        if not self.active:
            return None

        # Key input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]

            elif event.key == pygame.K_RETURN:
                return "enter"

            else:
                # event.unicode is the typed character
                if event.unicode.isprintable():
                    self.text += event.unicode

        return None
    
    def draw(self, screen):
        color = self.active_color if self.active else self.idle_color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)

        padding_x = 12
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + padding_x, self.rect.y + (self.rect.height - text_surface.get_height()) // 2))