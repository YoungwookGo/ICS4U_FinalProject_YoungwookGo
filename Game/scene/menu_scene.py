import pygame
from scene.base_scene import Scene
from scene.game_scene import GameScene

class MenuScene(Scene):
    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height

        self.title_font = pygame.font.SysFont("arial", 60)
        self.button_font = pygame.font.SysFont("arial", 36)

        btn_w = 220
        btn_h = 70
        btn_x = (width - btn_w) // 2
        btn_y = (height - btn_h) // 2

        self.start_button = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

    def handle_events(self, events):

        for event in events:
            if event.type == pygame.QUIT:
                self.next_scene = "QUIT"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.start_button.collidepoint(event.pos):
                    self.next_scene = GameScene(self.width, self.height)

    def update(self):
            pass

    def draw(self, screen):
        screen.fill((30, 30, 30))

        # 타이틀
        title_surface = self.title_font.render("Typing Game", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.width // 2, self.height // 2 - 120))
        screen.blit(title_surface, title_rect)

        # 버튼
        pygame.draw.rect(screen, (70, 70, 70), self.start_button)
        pygame.draw.rect(screen, (200, 200, 200), self.start_button, 3)

        button_text = self.button_font.render("START", True, (255, 255, 255))
        text_rect = button_text.get_rect(center=self.start_button.center)
        screen.blit(button_text, text_rect)

