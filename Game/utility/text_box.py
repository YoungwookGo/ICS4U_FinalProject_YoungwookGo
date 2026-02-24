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

        self.cursor_timer = 0
        self.cursor_interval = 0.5
        self.cursor_visible = True

    def locate(self, x, y):
        # Set location of the text box's center
        self.rect.center = (x, y)

    def update(self, dt):
        """
        Update cursor blinking using delta time.
        """
        if not self.active:
            return

        self.cursor_timer += dt

        if self.cursor_timer >= self.cursor_interval:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

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

        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (self.rect.x + padding_x, text_y))

        # --- Draw cursor ---
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + padding_x + text_surface.get_width() + 3
            cursor_y = text_y + 5
            cursor_height = text_surface.get_height() - 10

            pygame.draw.line(
                screen,
                self.text_color,
                (cursor_x, cursor_y),
                (cursor_x, cursor_y + cursor_height),
                3
            )