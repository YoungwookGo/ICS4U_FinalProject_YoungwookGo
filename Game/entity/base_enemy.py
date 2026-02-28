import pygame

class Enemy(pygame.sprite.Sprite):
    """
    Base class for all enemies.
    Have basic properties.
    Handle movement and visual.
    """

    BASE_COLOR = (255, 255, 255)
    BASE_SPEED = 120
    BASE_HP = 1

    def __init__(self, game, y, speed_adj = 0, word = None):
        # Call initialize method from parent class
        super().__init__()
        
        self.game = game
        self.font = pygame.font.Font("Game/asset/font/NotoSans-SemiBold.ttf", 40)

        self.text_color = self.BASE_COLOR
        self.hp = self.BASE_HP

        self.passed = False

        self.speed_adj = speed_adj
        
        if word is None:
            self.new_word()
            self.speed = self.calculate_speed() + self.speed_adj
            self._rerender()
        else:
            self.word = word
            self.speed = self.calculate_speed() + self.speed_adj
            self._rerender()

        start_x = -20
        self.rect = self.image.get_rect(midleft=(start_x, y))
        self._x = float(self.rect.x)

    # Word ===============================================================

    def new_word(self):
        self.word = self.game.scene.word_api.get_word() or "ohno"

    # Combat =============================================================
    
    def take_damage(self):
        """
        Called when user types this enemy correctly.
        Returns True if this hit kills the enemy.
        """
        self.hp -= 1
        if self.hp > 0:
            self.damage_effect()
            return False
        return True
    
    def damage_effect(self):
        """Called when get damage but not dead yet."""
        return
    
    def exit_effect(self, scene):
        """
        Called when the player types this enemy correctly.
        Default is doing nothing. Subclasses override this.
        """
        return

    # Movement ===========================================================

    def calculate_speed(self) -> float:
        """Calculate enemy speed from word length"""
        base_len = 6
        min_speed = 30
        max_speed = 200

        L = max(1, len(self.word))
        speed = self.BASE_SPEED * (base_len / L)

        # clamp
        if speed < min_speed:
            speed = min_speed
        elif speed > max_speed:
            speed = max_speed

        return speed
    
    def update(self, dt):
        # Keep moving right
        self._x += self.speed * dt
        self.rect.x = int(self._x)

        # Detect if it reached right edge
        if self.rect.left > self.game.WIDTH:
            self.passed = True

    # ====================================================================

    def _rerender(self):
        self.image = self.font.render(self.word, True, self.text_color)