import pygame
import os
import random
from scene.base_scene import Scene
from utility.text_box import TextBox
from utility.random_word import RandomWord
from utility.statistic import StatsManager
from entity.enemy1 import Enemy1
from entity.enemy2 import Enemy2
from entity.enemy3 import Enemy3


class GameScene(Scene):
    """
    Main game scene class for the program.
    """

    def __init__(self, game):
        # Call initialize method from parent class
        super().__init__(game)

        # Call utility --------------------------
        self.word_api = RandomWord()
        self.stats = StatsManager()

        # Font ----------------------------------
        self.input_font = pygame.font.Font(
            os.path.join("Game", "asset", "font", "NotoSans-Medium.ttf"), 48)
        self.ui_font = pygame.font.Font(
            os.path.join("Game","asset","font","NotoSans-SemiBold.ttf"), 32)
        
        # Game variables ------------------------
        self.init_hp = 5
        self.hp = self.init_hp

        self.score = 0
        self.combo = 0

        self.stage = 14

        self.energy = 0

        # Stat variables ------------------------
        self.max_combo = 0
        self.kill_count = 0

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

        bg_idx = (self.stage - 1) % len(self.bg_images)
        self.background = self.bg_images[bg_idx]

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
            y = 200 + i * 120
            word = self.word_api.get_word() or "ohno"
            enemy = Enemy1(self.game, y, word=word)
            self.enemies.add(enemy)

    # ====================================================================

    def manage_event(self, events):
        # Call manage_event method from parent class
        super().manage_event(events)

        # Manage every events from referenced classes
        for event in events:
            # Manage events in text_box class -----------------------
            # Skill 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                self.skill1()
                continue

            # Text enter
            result = self.text_box.interact(event)
            if result == "enter":
                self.check_input()

    # ====================================================================

    def check_input(self):
        # Case sensitive
        text_input = self.text_box.text.strip()

        # Do nothing when text input is empty
        if text_input == "":
            return

        # Check each enemy with user input
        for enemy in self.enemies:
            if enemy.word == text_input:
                die = enemy.take_damage()

                if die:
                    # Common events on enemy defeat
                    self.defeat_enemy(enemy)

                    # Energy increases only when user defeat enemy by typing
                    self.energy += 10

                    # Combo increases only when user defeat enemy by typing
                    self.combo += 1
                    if self.combo > self.max_combo:
                        self.max_combo = self.combo
                break
        else:
            # When there is no word matching with input
            self.combo = 0

        self.text_box.text = ""

    def skill1(self):
        """Remove all enemies on screen and respawn them with new words."""
        if self.energy < 100:
            return  # not ready
    
        self.energy -= 100

        for enemy in self.enemies:
            die = enemy.take_damage()

            if die:
                # Common events on enemy defeat
                self.defeat_enemy(enemy)
            
    # ====================================================================

    def defeat_enemy(self, enemy):
        """Manage events when an enemy is defeated."""

        # Manage score
        gained = 10 + self.combo + (self.stage - 1) 
        self.score += gained

        # Manage statistics
        self.kill_count += 1

        # Manage background
        if self.kill_count >= self.stage * 20:
            self.stage = self.kill_count // 20 + 1
            bg_idx = (self.stage - 1) % len(self.bg_images)
            self.background = self.bg_images[bg_idx]

        # Manage loot and exit effect
        enemy.exit_effect(self)

        # Reset enemy
        y = enemy.rect.centery
        enemy.kill()
        new_enemy = self.spawn_enemy(y)
        self.enemies.add(new_enemy)


    def spawn_enemy(self, y):
        speed_adj = (self.stage - 1) * 10

        r = random.random()
        if r < 0.10:
            return Enemy3(self.game, y, speed_adj=speed_adj)
        elif r < 0.20:
            return Enemy2(self.game, y, speed_adj=speed_adj)
        else:
            return Enemy1(self.game, y, speed_adj=speed_adj)
        
    # ====================================================================

    def update(self):
        dt = self.game.clock.get_time() / 1000
        self.enemies.update(dt)
        self.text_box.update(dt)

        for enemy in list(self.enemies):
            if enemy.passed:
                self.hp -= 1

                y = enemy.rect.centery
                enemy.kill()
                new_enemy = self.spawn_enemy(y)
                self.enemies.add(new_enemy)

                enemy.passed = False

            if self.hp <= 0:
                # Game over
                self.game.last_score = self.score
                self.request_scene = "over"
                # Statistics renewal
                self.stats.increment_total_games()
                self.game.is_high_score = self.stats.submit_score(self.score)
                print(self.game.is_high_score)
                self.game.high_score = self.stats.get_achievement("high_score")
                print(self.game.high_score)
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
        energy_surf = self.ui_font.render(f"Energy: {self.energy}", True, (255, 255, 255))

        kill_surf = self.ui_font.render(f"Kill: {self.kill_count}", True, (255, 255, 255))


        screen.blit(hp_surf, (20, 10))
        screen.blit(score_surf, (200, 10))
        screen.blit(combo_surf, (400, 10))
        screen.blit(energy_surf, (600, 10))

        screen.blit(kill_surf, (20, 45))
