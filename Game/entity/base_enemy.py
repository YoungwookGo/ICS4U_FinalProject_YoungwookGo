import pygame

class Enemy(pygame.sprite.Sprite):
    """
    Base class for all enemies.
    Have basic properties.
    Handle movement and visual.
    """

    def __init__(self, game, word, x, y, base_speed):
        super().__init__()
        
        self.game = game
        self.base_speed = base_speed

        self.font = pygame.font.Font("Game/asset/font/NotoSans-SemiBold.ttf", 40)

        self.word = word
        self.speed = self.calculate_speed(self.word)

        self.image = self.font.render(self.word, True, (255, 255, 255))
        self.rect = self.image.get_rect(midleft=(x, y))

        self._x = float(self.rect.x) # Smooth movement
        self._y = y

        self.passed = False

    def update(self, dt):
        # Move right
        self._x += self.speed * dt
        self.rect.x = int(self._x)

        if self.rect.left > self.game.WIDTH:
            self.passed = True

    def reset(self, new_word, y=None):
        """Respawn this enemy at the left with a new word."""
        if y is None:
            y = self.rect.centery

        self.word = new_word
        self.image = self.font.render(self.word, True, (255, 255, 255))
        self.rect = self.image.get_rect(midleft=(-20, y))
        
        self._x = float(self.rect.x)
        self.passed = False

    def calculate_speed(self, word: str) -> float:
        target_len = 6
        min_speed = 30
        max_speed = 200

        L = max(1, len(word))
        speed = self.base_speed * (target_len / L)

        # clamp
        if speed < min_speed:
            speed = min_speed
        elif speed > max_speed:
            speed = max_speed

        return speed