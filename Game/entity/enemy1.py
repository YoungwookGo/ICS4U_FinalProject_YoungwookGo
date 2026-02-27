from entity.base_enemy import Enemy

class Enemy1(Enemy):
    """
    Basic enemy type
    """

    def __init__(self, game, word, y):
        super().__init__(game, word, y)