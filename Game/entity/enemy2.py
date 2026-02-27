from entity.base_enemy import Enemy

class Enemy2(Enemy):
    """
    Fast enemy type
    - Faster speed
    - Provide more energy when defeated
    """

    BASE_COLOR = (0, 255, 200)
    BASE_SPEED = 300

    def __init__(self, game, y, word: None):
        super().__init__(game, y, word)

        self.text_color = self.BASE_COLOR
        self.image = self.font.render(self.word, True, self.text_color)

    def exit_effect(self, scene):
        scene.energy += 90
    