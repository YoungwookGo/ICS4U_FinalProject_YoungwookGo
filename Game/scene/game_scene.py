# #####################################
# Class Name:   GameScene
# Course:       ICS4U 
# Author:       Youngwook Go 
# Date:         2026-03-05
# File Name:    game_scene.py
# Description:  
#   GameScene is the main gameplay scene for the typing game.
#    - Spawn and update moving word enemies using a Sprite Group.
#    - Collect typing input through a TextBox and check against enemies.
#    - Track gameplay stats (score, combo, kills, stage, energy, durability).
#    - Save statistics and high score when the game ends.
# #####################################
import pygame
import os
import random

from scene.base_scene import Scene
from utility.button import IconButton
from utility.random_word import RandomWord
from utility.statistic import StatsManager
from utility.textbox import TextBox
from utility.overlay_menu import OverlayMenuManager, PauseOverlayMenu, GuideOverlayMenu
from entity.enemy import Enemy1, Enemy2, Enemy3

class GameScene(Scene):
    """
    Main game scene class for the program.
    """

    # Gameplay tuning
    INIT_DURABILITY = 5
    ENERGY_PER_KILL = 10
    SKILL1_COST = 100

    BASE_SCORE = 10
    SCORE_STAGE_BONUS = 1  # added as (stage - 1) * SCORE_STAGE_BONUS
    SCORE_COMBO_BONUS = 1  # added as combo * SCORE_COMBO_BONUS

    START_ENEMY_COUNT = 3
    ENEMY_START_Y = 200
    ENEMY_Y_GAP = 120

    # Stage logic
    KILLS_PER_STAGE = 20
    SPEED_ADJ_PER_STAGE = 10

    # Enemy spawn probabilities
    # 10% Enemy3, next 10% Enemy2, otherwise Enemy1
    ENEMY3_RATE = 0.10
    ENEMY2_RATE = 0.20

    # Background filename list
    BG_FILES = [
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

    # =========================================================================
    # Initialize section
    # =========================================================================

    def __init__(self, game):
        """
        Initialize the gameplay scene.
        """
        # Call initialize method from parent class
        super().__init__(game)

        # Call utility
        self.word_api = RandomWord()
        self.stats = StatsManager()
        
        # Core gameplay state
        self.init_durability = self.INIT_DURABILITY
        self.durability = self.init_durability

        self.score = 0
        self.combo = 0
        self.stage = 1
        self.energy = 0

        self.paused = False

        # Stat variables 
        self.max_combo = 0
        self.kill_count = 0

        # Initialize background images
        self.bg_images = self._load_backgrounds()
        self.background = self.bg_images[0] if self.bg_images else None

        # Update background image once
        self.update_background()

        # Initialize overlay menus
        self.overlay_menu = OverlayMenuManager(self.game, self)
        self.overlay_menu.register("paused", PauseOverlayMenu(self.game, self))
        self.overlay_menu.register("guide", GuideOverlayMenu(self.game, self))

        # Initialize pause button
        self.pause_button = IconButton(
            font=self.icon_font,
            text="☰",
            size=(50,50),
            text_color=self.TEXT_COLOR_DARK,
            idle_color=self.BUTTON_COLOR_IDLE,
            active_color=self.BUTTON_COLOR_ACTIVE,
        )
        self.pause_button.locate(self.game.WIDTH - 30, 30)

        # Initialize text box
        self.textbox = TextBox(
            font=self.inputbox_font,
            size=self.TEXTBOX_SIZE,
            text_color=self.TEXT_COLOR_DARK,
            idle_color=self.BUTTON_COLOR_IDLE,
            active_color=self.BUTTON_COLOR_ACTIVE,
        )
        self.textbox.locate(self.center_x, self.game.HEIGHT - 80)

        # Initialize enemy sprite group
        self.enemies = pygame.sprite.Group()
        self._spawn_init_enemies()
    #end __init__()

    def _load_backgrounds(self):
        """
        Load and scale background images.
        """
        images = []
        for filename in self.BG_FILES: # Background image file lists
            path = os.path.join(self.WALLPAPER_DIR, filename)
            try:
                img = pygame.image.load(path).convert()
                img = pygame.transform.scale(img, (self.game.WIDTH, self.game.HEIGHT))
                images.append(img)
            except (pygame.error, OSError):
                # If one image fails, skip it but keep the game running.
                print(f"GameScene ERROR: Failed to load background -> {path}")

        # Return list of loaded image.
        return images
    #end _load_backgrounds()

    def _spawn_init_enemies(self):
        """
        Spawn the initial enemies at fixed lane positions.
        """
        for i in range(self.START_ENEMY_COUNT):
            y = self.ENEMY_START_Y + i * self.ENEMY_Y_GAP
            word = self.word_api.get_word() or "ohno"
            enemy = Enemy1(self.game, y, word=word)
            self.enemies.add(enemy)
    #end _spawn_init_enemies()

    # =========================================================================
    # END Initialize section
    # =========================================================================

    def spawn_enemy(self, y):
        """
        Spawn an enemy based on current stage and spawn probabilities.
        """
        speed_adj = (self.stage - 1) * self.SPEED_ADJ_PER_STAGE

        r = random.random()
        if r < 0.10:
            return Enemy3(self.game, y, speed_adj=speed_adj)
        elif r < 0.20:
            return Enemy2(self.game, y, speed_adj=speed_adj)
        else:
            return Enemy1(self.game, y, speed_adj=speed_adj)
    #end spawn_enemy()
    
    def check_input(self):
        """
        Check the player's typed word against current enemies.
        """
        # Case sensitive
        text_input = self.textbox.get_text().strip()

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

        self.textbox.clear()
    #end check_input()

    def skill1(self):
        """
        Remove all enemies on screen and respawn them with new words.
        """
        if self.energy < self.SKILL1_COST:
            return  # not ready
    
        self.energy -= self.SKILL1_COST

        # Iterate on a copy because enemies will be removed and replaced
        for enemy in list(self.enemies):
            die = enemy.take_damage()

            if die:
                # Common events on enemy defeat
                self.defeat_enemy(enemy)
    #end skill1()

    def defeat_enemy(self, enemy):
        """
        Manage events when an enemy is defeated.
        """

        # Score formula (easy to explain in report)
        gained = (
            self.BASE_SCORE
            + self.combo * self.SCORE_COMBO_BONUS
            + (self.stage - 1) * self.SCORE_STAGE_BONUS
        )
        self.score += gained

        # Manage statistics
        self.kill_count += 1

        # Stage update is based on kill count
        self.stage = (self.kill_count // self.KILLS_PER_STAGE) + 1
        self.update_background()

        # Manage loot and exit effect
        enemy.exit_effect(self)

        # Reset enemy
        lane_y = enemy.rect.centery
        enemy.kill()

        new_enemy = self.spawn_enemy(lane_y)
        self.enemies.add(new_enemy)
    #end defeat_enemy()
    
    def update_background(self):
        """
        Update the background based on the current stage.
        """
        if not self.bg_images:
            self.background = None
            return

        index = (self.stage - 1) % len(self.bg_images)
        self.background = self.bg_images[index]
    #end update_background()

    def game_over(self):
        """
        Save statistics and request transition to OverScene.
        """
        self.game.last_score = self.score

        # Statistics saving
        self.stats.increment_total_games()
        self.game.is_high_score = self.stats.submit_score(self.score)
        print("Is High Score: ", self.game.is_high_score)

        # Sync high score value from StatsManager
        self.game.high_score = self.stats.get_achievement("high_score")
        print("High Score: ", self.game.high_score)

        # Request scene transition
        self.request_scene = self.OVER_SCENE
    #end game_over()

    def set_paused(self, paused):
        """
        Sync paused state with input availability.
        """
        self.paused = paused
        self.textbox.active = not paused
        if paused:
            self.overlay_menu.open("paused")
        else:
            self.overlay_menu.close()
    #end set_paused()

    def manage_event(self, events):
        """
        Handle input events in textbox class.
        - TAB: Activate Skill 1
        - Enter: Submit typed word
        """
        # Call manage_event method from parent class
        super().manage_event(events)

        # Manage every events from referenced classes
        for event in events:
            # 1) Pause game with button or escape key
            if self.pause_button.interact(event):
                self.set_paused(not self.paused)
                continue

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.set_paused(not self.paused)
                continue

            # 2) If paused, handle menu events from overlay menu
            if self.paused:
                action = self.overlay_menu.handle_event(event)
                self._manage_overlay_event(action)
                continue

            # 3) Normal gameplay inputs
            if event.type == pygame.KEYDOWN:
                # Skill 1
                if event.key == pygame.K_TAB:
                    self.skill1()
                    continue

            # 4) Textbox input
            result = self.textbox.interact(event)
            if result == "enter":
                self.check_input()
    #end manage_event()

    def _manage_overlay_event(self, action):
        """
        Handle action returned from the currently active overlay menu.
        Returns True when an action was handled.
        """
        if action is None:
            return False

        if action == "quit":
            self.request_quit = True
            return True
        elif action == "guide":
            self.overlay_menu.open("guide")
            return True
        elif action == "back":
            self.overlay_menu.open("paused")
            return True
        elif action == "game_over":
            self.game_over()
            return True
        elif action == "continue":
            self.set_paused(False)
            return True
        elif action == "resume_by_key":
            self.set_paused(False)
            return True
        else:
            return False
    #end _manage_overlay_event()

    def update(self):
        """
        Update enemies, input UI, and handle game-over conditions.
        """
        if self.paused:
            return
    
        dt = self.game.clock.get_time() / 1000

        # Update entities
        self.enemies.update(dt)
        self.textbox.update(dt)

        # Handle enemies that passed the screen edge
        for enemy in list(self.enemies):
            if enemy.passed:
                self.durability -= 1

                y = enemy.rect.centery
                enemy.kill()

                new_enemy = self.spawn_enemy(y)
                self.enemies.add(new_enemy)

                enemy.passed = False

                # Reset combo when the player misses an enemy
                self.combo = 0

        # Game over check run once per frame.
        if self.durability <= 0:
            self.game_over()
    #end update()

    def draw(self, screen):
        """
        Draw background, enemies, input box, and UI HUD.
        """
        # Reset screen
        screen.blit(self.background, (0, 0))

        # Draw enemy
        self.enemies.draw(screen)

        # Draw button
        self.pause_button.draw(screen)

        # Draw text box only during active gameplay
        if not self.paused:
            self.textbox.draw(screen)

        # Draw test
        durability_surf = self.content_font.render(
            f"Durability: {self.durability}/{self.init_durability}", True, self.TEXT_COLOR_RED)
        
        score_surf = self.content_font.render(
            f"Score: {self.score}", True, self.TEXT_COLOR_CYAN)
        
        combo_surf = self.content_font.render(
            f"Combo: {self.combo}", True, self.TEXT_COLOR_CYAN)
        
        energy_surf = self.content_font.render(
            f"Energy: {self.energy}", True, self.TEXT_COLOR_YELLOW)
        
        kill_surf = self.content_font.render(
            f"Kills: {self.kill_count}", True, self.TEXT_COLOR_YELLOW)

        screen.blit(durability_surf, (20, 10))
        screen.blit(score_surf, (300, 10))
        screen.blit(combo_surf, (500, 10))
        screen.blit(energy_surf, (720, 10))
        screen.blit(kill_surf, (950, 10))

        # Overdraw pause menu when paused
        if self.paused:
            self.overlay_menu.draw(screen)
    #end draw()
