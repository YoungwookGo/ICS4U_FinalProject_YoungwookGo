import pygame
from scene.base_scene import Scene
from utility.text_box import TextBox
from utility.random_word import RandomWord
from entity.enemy1 import Enemy1

class GameScene(Scene):
    """
    Main game scene class for the program.
    """

    def __init__(self, game):
        super().__init__(game)

        # Visuals -------------------------------
        self.input_font = pygame.font.Font("Game/asset/font/NotoSans-Medium.ttf", 48)
        self.ui_font = pygame.font.Font("Game/asset/font/NotoSans-SemiBold.ttf", 32)

        self.text_box = TextBox(
            font=self.input_font,
            size=(1000, 80),
            text_color=(255, 255, 255),
            idle_color=(70, 70, 80),
            active_color=(110, 110, 130),
        )

        # Utilities -----------------------------
        self.word_api = RandomWord()

        # Entities ------------------------------
        self.enemies = pygame.sprite.Group()
        for i in range(3):
            word = self.word_api.get_word() or "offline"
            y = 200 + i * 120
            enemy = Enemy1(self.game, word, y)
            self.enemies.add(enemy)

        # Game functions ------------------------
        self.score = 0
        self.combo = 0
        self.max_combo = 0

        

    def manage_event(self, events):
        super().manage_event(events)

        for event in events:
            # Check text enter
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
                # Score manage
                self.combo += 1
                if self.combo > self.max_combo:
                    self.max_combo = self.combo

                gained = 10 + self.combo
                self.score += gained

                # Game function
                y = enemy.rect.centery
                enemy.kill()

                new_word = self.word_api.get_word() or "OHNO"
                self.enemies.add(Enemy1(self.game, new_word, y))
                print("Typed right")
                break
        else:
            # Runs when for loop don't breaks
            self.combo = 0
            print("Typed wrong")

        self.text_box.text = ""

    def update(self):
        dt = self.game.clock.get_time() / 1000  # milliseconds -> seconds
        self.enemies.update(dt)

    def draw(self, screen):
        # Reset screen
        screen.fill((10, 10, 15))

        # Define center guideline
        center_x = self.game.WIDTH // 2
        center_y = self.game.HEIGHT // 2

        # Text box
        self.text_box.locate(center_x, self.game.HEIGHT - 80)
        self.text_box.draw(screen)

        # Enemy
        self.enemies.draw(screen)

        # UI
        score_surf = self.ui_font.render(f"Score: {self.score}", True, (255, 255, 255))
        combo_surf = self.ui_font.render(f"Combo: {self.combo}", True, (255, 255, 255))
        comboM_surf = self.ui_font.render(f"Max Combo: {self.max_combo}", True, (255, 255, 255))

        screen.blit(score_surf, (15, 10))
        screen.blit(combo_surf, (15, 50))
        screen.blit(comboM_surf, (15, 90))