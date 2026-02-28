from entity.base_enemy import Enemy

class Enemy1(Enemy):
    """
    Basic enemy type
    """

    def __init__(self, game, y, word = None):
        super().__init__(game, y, word)