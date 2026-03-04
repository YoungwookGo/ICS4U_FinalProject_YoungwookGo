# #####################################
# Class Name:   Enemy / Enemy1 / Enemy2 / Enemy3
# Course:       ICS4U 
# Author:       Youngwook Go 
# Date:         2026-03-01
# File Name:    enemy.py
# Description:  
#    Enemy is the super class designed using OOP inheritance.
#
#    Subclasses (Enemy1, Enemy2, Enemy3) extend this class
#    and override specific behaviors such as speed and rewards.
##############################################

# Python library for building 2D games.
import pygame

class Enemy(pygame.sprite.Sprite):
    """
    Base class for all enemies.
    Have basic properties.
    Handle movement and visual.
    """
    # Default enemy settings (subclasses can override these)
    BASE_COLOR = (255, 255, 255)
    BASE_SPEED = 120
    BASE_DURABILITY = 1 # asdf

    # Movement & speed calculation constants
    START_X = -20
    SPEED_BASE_WORD_LENGTH = 6
    MIN_SPEED = 30
    MAX_SPEED = 200

    def __init__(self, game, y, speed_adj = 0, word = None):
        """
        Initialize an Enemy object.
        """
        # Call initialize method from parent class
        super().__init__()
        
        self.game = game

        # Font used to render the word.
        self.font = pygame.font.Font("Game/asset/font/NotoSans-SemiBold.ttf", 40)

        # Core state
        self.text_color = self.BASE_COLOR
        self.durability = self.BASE_DURABILITY
        self.passed = False

        # Speed adjustment allows difficulty scaling.
        self.speed_adj = speed_adj
        
        # Set word, generate if not provided.
        if word is None:
            self.new_word()
        else:
            self.word = word

        # Calculate speed based on the word length and apply adjustment.
        self.speed = self.calculate_speed() + self.speed_adj

        # Render the word image and initialize position.
        self._render_text()

        self.rect = self.image.get_rect(midleft=(self.START_X, y))
        self._x = float(self.rect.x)
    #end __init__()

    def new_word(self):
        """
        Generate a new word using the game's word provider.
        If the API fails, use a safe fallback word.
        """
        self.word = self.game.scene.word_api.get_word() or "ohno"
    #end new_word()

    def take_damage(self):
        """
        Called when user types this enemy correctly.
        Returns True if this hit kills the enemy (typed word is correct).
        """
        self.durability -= 1
        if self.durability > 0:
            # Subclasses may override damage_effect() for visual or speed changes.
            self.damage_effect()
            return False
        return True
    #end take_damage()
    
    def damage_effect(self):
        """
        Called when the enemy is hit but not defeated yet.
        Default behavior: do nothing.
        Subclasses can override this for special effects.
        """
        return
    #end damage_effect()
    
    def exit_effect(self, scene):
        """
        Called when the player types this enemy correctly.
        Default is doing nothing. 
        Subclasses can override this to reward the player.
        """
        return
    #end exit_effect()

    def calculate_speed(self):
        """
        Calculate enemy speed based on the word length.
        """
        length = max(1, len(self.word))

        # Inverse relationship: shorter word -> faster speed
        speed = self.BASE_SPEED * (self.SPEED_BASE_WORD_LENGTH / length)

        # Clamp speed to keep gameplay fair and consistent.
        if speed < self.MIN_SPEED:
            speed = self.MIN_SPEED
        elif speed > self.MAX_SPEED:
            speed = self.MAX_SPEED

        return speed
    #end calculate_speed()
    
    def update(self, dt):
        """
        Update enemy movement.
        - dt: Delta time in seconds since last frame
        """
        # Keep moving right
        self._x += self.speed * dt
        self.rect.x = int(self._x)

        # Detect if it reached right edge of the screen.
        if self.rect.left > self.game.WIDTH:
            self.passed = True
    #end update()

    def _render_text(self):
        """
        Render the enemy's word into the screen.
        This method is called whenever word/color changes.
        """
        self.image = self.font.render(self.word, True, self.text_color)
    #end _render_text()
#end class Enemy

# ======================================================================
# Enemy types
# ======================================================================
class Enemy1(Enemy):
    """
    Basic enemy type
    """
    BASE_COLOR = (255, 255, 255)
    BASE_SPEED = 120

    def __init__(self, game, y, speed_adj = 0, word = None):
        super().__init__(game, y, speed_adj=speed_adj, word=word)
    #end __init__()
#end class Enemy1

# ====================================================================
class Enemy2(Enemy):
    """
    Fast enemy type
    - Faster speed
    - Provide more energy when defeated
    """

    BASE_COLOR = (0, 255, 200)
    BASE_SPEED = 300

    ENERGY_REWARD = 90

    def __init__(self, game, y, speed_adj=0, word=None):
        super().__init__(game, y, speed_adj=speed_adj, word=word)

        # Apply subclass color and re-render.
        self.text_color = self.BASE_COLOR
        self._render_text()
    #end __init__()

    def exit_effect(self, scene):
        """
        Reward energy when defeated.
        """
        scene.energy += self.ENERGY_REWARD
    #end exit_effect()
#end class Enemy2

# ====================================================================
class Enemy3(Enemy):
    """
    Tank enemy type
    - Need to typed correctly twice to be defeated
    - Provide a health when defeated
    """

    BASE_COLOR = (225, 0, 15)
    BASE_DURABILITY = 2

    # After taking the first hit, the enemy becomes slower.
    DAMAGED_SPEED_MULTIPLIER = 0.75

    # Color used after first hit (shows the enemy is damaged).
    DAMAGED_COLOR = (239, 65, 53)

    DURABILITY_REWARD = 1

    def __init__(self, game, y, speed_adj = 0, word = None):
        super().__init__(game, y, speed_adj=speed_adj, word=word)
    #end __init__()

    def take_damage(self):
        """
        1st correct input: change to a NEW word (enemy stays alive)
        2nd correct input: die
        """
        self.durability -= 1

        if self.durability > 0:
            # Change word and update visuals after the first hit.
            self.new_word()
            self.text_color = self.DAMAGED_COLOR

            # Recalculate speed and apply damaged multiplier.
            self.speed = (self.calculate_speed() + self.speed_adj) * self.DAMAGED_SPEED_MULTIPLIER

            # Re-render with new word and new color.
            self._render_text()
            return False

        return True
    #end take_damage()

    def exit_effect(self, scene):
        """
        Reward durability when defeated.
        """
        scene.durability += self.DURABILITY_REWARD
    #end exit_effect()
#end class Enemy3