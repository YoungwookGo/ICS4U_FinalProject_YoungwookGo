from entity.base_enemy import Enemy

class Enemy2(Enemy):
    """
    Unique enemy type
    - Provide more energy when killed
    """

    BASE_COLOR = (0, 255, 200)
    BASE_SPEED = 160

    def __init__(self, game, word, y):
        super().__init__(game, word, y)

        self.text_color = self.BASE_COLOR
        self.speed = self.calculate_speed(word)
        self.image = self.font.render(self.word, True, self.text_color)

    def exit_effect(self, scene):
        scene.energy += 50
    