import pygame

class Enemy(pygame.sprite.Sprite):
    """
    Base class for all enemies.
    Have basic properties.
    Handle movement and visual.
    """

    def __init__(self, game, word, x, y, speed):
        super().__init__()
        
        self.game = game
        self.word = word
        self.speed = speed

        self.x = x
        self.y = y

        self.font = pygame.font.Font("Game/asset/font/NotoSans-SemiBold.ttf", 40)
        self.image = self.font.render(self.word, True, (255, 255, 255))
        self.rect = self.image.get_rect(midleft=(x, y))

        self._x = float(self.rect.x) # Smooth movement

    def update(self, dt):
        # Move right
        self._x += self.speed * dt
        self.rect.x = int(self._x)

        # Remove if touch right edge
        if self.rect.left > self.game.WIDTH + 50:
            self.kill()