from entity.base_enemy import Enemy

class Enemy3(Enemy):
    """
    Tank enemy type
    - Need to typed correctly twice to be defeated
    - Provide a health when defeated
    """

    BASE_COLOR = (225, 0, 15)
    BASE_HP = 2

    DAMAGED_SPEED_MULTIPLIER = 0.75

    def __init__(self, game, y, speed_adj = 0, word = None):
        super().__init__(game, y, speed_adj=speed_adj, word=word)

    def take_damage(self):
        """
        1st correct input: change to a NEW word (enemy stays alive)
        2nd correct input: die
        """
        self.hp -= 1

        if self.hp > 0:
            self.new_word()
            self.text_color = (239, 65, 53)

            self.speed = (self.calculate_speed() + self.speed_adj) * self.DAMAGED_SPEED_MULTIPLIER

            self._rerender()

            return False

        return True
    
    def exit_effect(self, scene):
        scene.hp += 1