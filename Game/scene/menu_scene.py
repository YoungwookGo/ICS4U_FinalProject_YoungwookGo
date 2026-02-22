import pygame
from scene.base_scene import Scene

class MenuScene(Scene):
    """
    Main Menu Scene.
    Displays title and start button.
    """

    def __init__(self, game):
        """Initialize menu scene"""

        # Initialize
        super().__init__(game)

        # Fonts
        self.title_font = pygame.font.Font("Game/asset/font/NotoSans-SemiBold.ttf", 80)
        self.button_font = pygame.font.Font("Game/asset/font/NotoSans-SemiBold.ttf", 40)

        # Create surface
        self.title_surface = self.title_font.render("Typing Game", True, (255, 255, 255))
        self.button_surface = self.button_font.render("START", True, (0, 0, 0))

        # 버튼 크기
        self.button_rect = pygame.Rect(0, 0, 220, 70)


    def manage_event(self, events):
        super().manage_event(events)

        for event in events:
            if event.type == pygame.QUIT:
                self.request_quit = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.button_rect.collidepoint(event.pos):
                    self.request_scene = "game"

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((30, 30, 40))

        center_x = self.game.WIDTH // 2
        center_y = self.game.HEIGHT // 2

        # ----- Title -----
        title_rect = self.title_surface.get_rect(center=(center_x, center_y - 100))
        screen.blit(self.title_surface, title_rect)

        # ----- Button -----
        self.button_rect.center = (center_x, center_y + 20)

        pygame.draw.rect(screen, (200, 200, 200), self.button_rect, border_radius=8)
        text_rect = self.button_surface.get_rect(center=self.button_rect.center)
        screen.blit(self.button_surface, text_rect)