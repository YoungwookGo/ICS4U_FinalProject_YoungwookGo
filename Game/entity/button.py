import pygame

class Button:
    """
    Simple reusable button class
    - Have clickable rectangle
    - Detect interaction
    - Change color when moue hovers
    """

    def __init__(self, font, text, size, text_color, idle_color, active_color):
        self.font = font
        self.text = text

        self.text_color = text_color
        self.idle_color = idle_color
        self.active_color = active_color

        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.text_surface = self.font.render(self.text, True, self.text_color)

    def center(self, x, y):
        self.rect.center = (x, y)

    def interact(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )
    
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.active_color if self.rect.collidepoint(mouse_pos) else self.idle_color

        pygame.draw.rect(screen, color, self.rect, border_radius=8)

        # re-center text every draw (safe even if rect moves)
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, text_rect)