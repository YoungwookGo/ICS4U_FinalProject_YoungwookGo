from entity.base_enemy import Enemy

class Enemy1(Enemy):
    """
    Basic enemy type
    """

    BASE_COLOR = (255, 255, 255)
    BASE_SPEED = 120

    def __init__(self, game, y, speed_adj = 0, word = None):
        super().__init__(game, y, speed_adj=speed_adj, word=word)