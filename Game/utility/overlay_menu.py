import pygame

from utility.button import Button


class OverlayMenu:
    """
    Base type for overlay menus.
    """

    def __init__(self, game, scene):
        self.game = game
        self.scene = scene

        # Shared overlay screening
        self.overlay_screening = pygame.Surface((self.game.WIDTH, self.game.HEIGHT), pygame.SRCALPHA)
        self.overlay_screening.fill((0, 0, 0, 80))

        # Shared menu bar
        self.menu_bar_height = self.scene.BUTTON_SIZE[1] * 2
        
        menu_bar_size = (self.game.WIDTH, self.menu_bar_height)
        self.bar_surf = pygame.Surface(menu_bar_size, pygame.SRCALPHA)
        self.bar_surf.fill((0, 0, 0, 160))

        self.bar_rect = self.bar_surf.get_rect(
            centerx = self.scene.center_x,
            bottom = self.game.HEIGHT
        )

    def handle_event(self, event):
        return None

    def draw(self, screen):
        screen.blit(self.overlay_screening, (0, 0))


class PauseOverlayMenu(OverlayMenu):
    """
    Pause overlay menu.
    """

    def __init__(self, game, scene):
        super().__init__(game, scene)

        # Initialize overlay panel for pause menu
        menu_title_size = (int(self.game.WIDTH * 0.5), int(self.game.HEIGHT * 0.4))
        self.title_surf = pygame.Surface(menu_title_size)

        pygame.draw.rect(
            self.title_surf,
            self.scene.PAUSE_MENU_COLOR,
            self.title_surf.get_rect(),
            border_radius=24,
        )

        self.title_rect = self.title_surf.get_rect(
            centerx = self.scene.center_x,
            centery = (self.game.HEIGHT - self.menu_bar_height) // 2
        )

        # Initialize title text for pause menu
        self.paused_surf = self.scene.title_font.render(
            "PAUSED!", True, self.scene.TEXT_COLOR_DARK
        )
        self.paused_rect = self.paused_surf.get_rect(
            center=(self.title_rect.centerx, self.title_rect.centery - 40)
        )

        # Initialize content text for pause menu
        self.resume_surf = self.scene.content_font.render(
            "Press any key to resume", True, self.scene.TEXT_COLOR_DARK
        )
        self.resume_rect = self.resume_surf.get_rect(
            center=(self.scene.center_x, self.scene.center_y)
        )

        # Initialize buttons for pause menu
        self.continue_button = Button(
            font=self.scene.button_font,
            text="Continue",
            size=self.scene.BUTTON_SIZE,
            text_color=self.scene.TEXT_COLOR_DARK,
            idle_color=self.scene.START_BUTTON_COLOR_IDLE,
            active_color=self.scene.START_BUTTON_COLOR_ACTIVE,
        )
        self.gameover_button = Button(
            font=self.scene.button_font,
            text="Game Over",
            size=self.scene.BUTTON_SIZE,
            text_color=self.scene.TEXT_COLOR_DARK,
            idle_color=self.scene.BUTTON_COLOR_IDLE,
            active_color=self.scene.BUTTON_COLOR_ACTIVE,
        )

        # Locate buttons for pause menu
        button_bar_y = self.game.HEIGHT - self.scene.BUTTON_SIZE[1]

        self.scene.quit_button.locate(self.scene.center_x - 360, button_bar_y)
        self.scene.guide_button.locate(self.scene.center_x - 120, button_bar_y)
        self.gameover_button.locate(self.scene.center_x + 120, button_bar_y)
        self.continue_button.locate(self.scene.center_x + 360, button_bar_y)

    def handle_event(self, event):
        if self.scene.quit_button.interact(event):
            return "quit"
        if self.scene.guide_button.interact(event):
            return "guide"
        if self.gameover_button.interact(event):
            return "game_over"
        if self.continue_button.interact(event):
            return "continue"
        if event.type == pygame.KEYDOWN:
            return "resume_by_key"
        return None

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.bar_surf, self.bar_rect)
        screen.blit(self.title_surf, self.title_rect)
        screen.blit(self.paused_surf, self.paused_rect)
        screen.blit(self.resume_surf, self.resume_rect)

        self.scene.quit_button.draw(screen)
        self.scene.guide_button.draw(screen)
        self.gameover_button.draw(screen)
        self.continue_button.draw(screen)


class GuideOverlayMenu(OverlayMenu):
    """
    Guide overlay menu.
    """

    def __init__(self, game, scene):
        super().__init__(game, scene)

        # Initialize overlay panel for guide menu
        menu_title_size = (int(self.game.WIDTH - 120), int(self.game.HEIGHT - self.menu_bar_height - 120))
        
        self.panel_surf = pygame.Surface(menu_title_size)
        pygame.draw.rect(
            self.panel_surf,
            self.scene.PAUSE_MENU_COLOR,
            self.panel_surf.get_rect(),
            border_radius=24,
        )

        self.panel_rect = self.panel_surf.get_rect()
        self.panel_rect.centerx = self.scene.center_x
        self.panel_rect.centery = (self.game.HEIGHT - self.menu_bar_height) // 2

        # Guide content pages
        self.pages = [
            {
                "title": "introduction",
                "contents": [
                "Word Defender is a simple game you can practice typing skill.",
                ],
            },
            {
                "title": "how to play",
                "contents": [
                "Type correct word shown in the game screen",
                ],
            },
        ]
        self.page_index = 0
        self.page_cache = self._build_page_cache()
        self.page_indicator = self._build_page_indicator()

        # Initialize buttons for guide menu
        self.button_1 = Button(
            font=self.scene.button_font,
            text="Return",
            size=self.scene.BUTTON_SIZE,
            text_color=self.scene.TEXT_COLOR_DARK,
            idle_color=self.scene.BUTTON_COLOR_IDLE,
            active_color=self.scene.BUTTON_COLOR_ACTIVE,
        )
        self.button_2 = Button(
            font=self.scene.button_font,
            text="<  Prev",
            size=self.scene.BUTTON_SIZE,
            text_color=self.scene.TEXT_COLOR_DARK,
            idle_color=self.scene.BUTTON_COLOR_IDLE,
            active_color=self.scene.BUTTON_COLOR_ACTIVE,
        )
        self.button_3 = Button(
            font=self.scene.button_font,
            text="Next  >",
            size=self.scene.BUTTON_SIZE,
            text_color=self.scene.TEXT_COLOR_DARK,
            idle_color=self.scene.BUTTON_COLOR_IDLE,
            active_color=self.scene.BUTTON_COLOR_ACTIVE,
        )

        button_bar_y = self.game.HEIGHT - self.scene.BUTTON_SIZE[1]
        self.button_1.locate(self.scene.center_x - 240, button_bar_y)
        self.button_2.locate(self.scene.center_x, button_bar_y)
        self.button_3.locate(self.scene.center_x + 240, button_bar_y)

    def _build_page_cache(self):
        """
        Pre-render guide text surfaces and positions once.
        """
        cache = []
        title_center_x = self.panel_rect.centerx
        title_center_y = self.panel_rect.top + 70
        content_x = self.panel_rect.left + 50
        content_gap = 40

        for page in self.pages:
            title_surf = self.scene.title_font.render(
                page["title"].upper(), True, self.scene.TEXT_COLOR_DARK
            )
            title_rect = title_surf.get_rect(center=(title_center_x, title_center_y))

            content_blits = []
            content_y = title_rect.bottom
            for content in page["contents"]:
                if content == "":
                    content_y += content_gap // 2
                    continue

                content_surf = self.scene.content_font.render(
                    content, True, self.scene.TEXT_COLOR_DARK
                )
                content_blits.append((content_surf, (content_x, content_y)))
                content_y += content_gap

            cache.append({
                "title_surf": title_surf,
                "title_rect": title_rect,
                "content_blits": content_blits,
            })
        return cache

    def _build_page_indicator(self):
        """
        Pre-render page number surfaces once.
        """
        indicator = []
        total = len(self.pages)
        center = (self.scene.center_x, self.bar_rect.top - 28)
        for i in range(total):
            surf = self.scene.content_font.render(
                f"{i + 1}/{total}", True, self.scene.TEXT_COLOR_LIGHT
            )
            rect = surf.get_rect(center=center)
            indicator.append((surf, rect))
        return indicator

    def handle_event(self, event):
        if self.button_1.interact(event):
            return "back"
        if self.button_2.interact(event):
            self.page_index = max(0, self.page_index - 1)
        if self.button_3.interact(event):
            self.page_index = min(len(self.pages) - 1, self.page_index + 1)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back"
        return None

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.bar_surf, self.bar_rect)
        screen.blit(self.panel_surf, self.panel_rect)

        # Draw current page title + content
        page = self.page_cache[self.page_index]
        screen.blit(page["title_surf"], page["title_rect"])
        for content_surf, content_pos in page["content_blits"]:
            screen.blit(content_surf, content_pos)

        # Draw page indicator above menu bar
        indicator_surf, indicator_rect = self.page_indicator[self.page_index]
        screen.blit(indicator_surf, indicator_rect)

        self.button_1.draw(screen)
        self.button_2.draw(screen)
        self.button_3.draw(screen)

class OverlayMenuManager:
    """
    Controls multiple overlay menu types.
    """

    def __init__(self, game, scene):
        self.game = game
        self.scene = scene
        self.menus = {}
        self.active_name = None

    def register(self, name, menu):
        self.menus[name] = menu

    def open(self, name):
        if name in self.menus:
            self.active_name = name

    def close(self):
        self.active_name = None

    def is_open(self):
        return self.active_name is not None

    def handle_event(self, event):
        if not self.is_open():
            return None
        return self.menus[self.active_name].handle_event(event)

    def draw(self, screen):
        if not self.is_open():
            return
        self.menus[self.active_name].draw(screen)
