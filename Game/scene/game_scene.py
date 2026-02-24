import pygame
import os
from scene.base_scene import Scene
from utility.text_box import TextBox
from utility.random_word import RandomWord
from utility.statistic import StatsManager
from entity.enemy1 import Enemy1


class GameScene(Scene):
    """
    Main game scene class for the program.
    """

    def __init__(self, game):
        # Call initialize method from parent class
        super().__init__(game)

        # Utilities -----------------------------
        self.word_api = RandomWord()
        self.stats = StatsManager()

        # Font ----------------------------------
        self.input_font = pygame.font.Font(
            os.path.join("Game", "asset", "font", "NotoSans-Medium.ttf"), 48)
        self.ui_font = pygame.font.Font(
            os.path.join("Game","asset","font","NotoSans-SemiBold.ttf"), 32)

        # Background ----------------------------
        self.bg_files = [
            "Solar_gradients_01.jpg",
            "Solar_gradients_02.jpg",
            "Solar_gradients_03.jpg",
            "Solar_gradients_04.jpg",
            "Solar_gradients_05.jpg",
            "Solar_gradients_06.jpg",
            "Solar_gradients_07.jpg",
            "Solar_gradients_08.jpg",
            "Solar_gradients_09.jpg",
            "Solar_gradients_10.jpg",
            "Solar_gradients_11.jpg",
            "Solar_gradients_12.jpg",
            "Solar_gradients_13.jpg",
            "Solar_gradients_14.jpg",
            "Solar_gradients_15.jpg",
            "Solar_gradients_16.jpg",
        ]

        self.bg_images = []

        for filename in self.bg_files:
            path = os.path.join("Game", "asset", "wallpaper", filename)
            img = pygame.image.load(path).convert()
            img = pygame.transform.scale(img, (self.game.WIDTH, self.game.HEIGHT))
            self.bg_images.append(img)

        self.background = self.bg_images[0]

        # UI ------------------------------------
        self.text_box = TextBox(
            font=self.input_font,
            size=(1000, 80),
            text_color=(255, 255, 255),
            idle_color=(70, 70, 80),
            active_color=(110, 110, 130),
        )

        # Entities ------------------------------
        self.enemies = pygame.sprite.Group()
        for i in range(3):
            word = self.word_api.get_word() or "ohno"
            y = 200 + i * 120
            enemy = Enemy1(self.game, word, y)
            self.enemies.add(enemy)

        # Game variables ------------------------
        self.init_hp = 5
        self.hp = self.init_hp

        self.score = 0
        self.combo = 0

        self.stage = 1

        # Statistic variables -------------------
        self.max_combo = 0
        self.kill_count = 0

    def manage_event(self, events):
        # Call manage_event method from parent class
        super().manage_event(events)

        # Manage every events from referenced classes
        for event in events:
            # Manage events in text_box class
            result = self.text_box.interact(event)
            if result == "enter":
                print("Typed:", self.text_box.text)
                self.check_input()

    def check_input(self):
        text_input = self.text_box.text.strip().lower()

        if text_input == "":
            return

        for enemy in self.enemies:
            if enemy.word.lower() == text_input:
                # Score management --------------
                gained = 10 + self.combo + (self.stage - 1) 
                self.score += gained

                self.combo += 1
                if self.combo > self.max_combo:
                    self.max_combo = self.combo

                self.kill_count +=1
                if self.kill_count >= self.stage * 20:
                    self.stage = self.kill_count // 20 + 1
                    bg_idx = (self.stage - 1) % len(self.bg_images)
                    self.background = self.bg_images[bg_idx]

                # Reset enemy -----------------
                new_word = self.word_api.get_word() or "ohno"
                enemy.reset(new_word, enemy.rect.centery)

                break
        else:
            # When there is no word matching with input
            self.combo = 0

        self.text_box.text = ""


    def update(self):
        dt = self.game.clock.get_time() / 1000
        self.enemies.update(dt)
        self.text_box.update(dt)

        for enemy in self.enemies:
            if enemy.passed:
                self.hp -= 1

                new_word = self.word_api.get_word() or "ohno"
                enemy.reset(new_word, enemy.rect.centery)

                enemy.passed = False

            if self.hp <= 0:
                # Game over
                self.request_scene = "menu"
                # Statistics renewal
                self.stats.increment_total_games()
                new_record = self.stats.submit_score(self.score)
                return

    def draw(self, screen):
        # Draw background image
        screen.blit(self.background, (0, 0))

        # Define center guideline
        center_x = self.game.WIDTH // 2
        center_y = self.game.HEIGHT // 2

        # Text box
        self.text_box.locate(center_x, self.game.HEIGHT - 80)
        self.text_box.draw(screen)

        # Enemy
        self.enemies.draw(screen)

        # UI
        hp_surf = self.ui_font.render(f"HP: {self.hp}/{self.init_hp}", True, (255, 255, 255))
        score_surf = self.ui_font.render(f"Score: {self.score}", True, (255, 255, 255))
        combo_surf = self.ui_font.render(f"Combo: {self.combo}", True, (255, 255, 255))

        screen.blit(hp_surf, (20, 10))
        screen.blit(score_surf, (200, 10))
        screen.blit(combo_surf, (400, 10))