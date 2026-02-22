import pygame
from scene.base_scene import Scene

class GameScene(Scene):
    """
    Main game scene class for the program.
    """

    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 36)

    def manage_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.request_quit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # 선택 1) 게임 종료
                    # self.request_quit = True

                    # 선택 2) 메뉴로 돌아가기 (추천)
                    self.request_scene = "menu"

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        text = self.font.render("GAME: ESC = Menu", True, (255, 255, 255))
        screen.blit(text, (20, 20))