class Scene:
    """
    Basic structure of every scene.
    All scenes should have:
    - handle_events()
    - update()
    - draw()
    """

    def __init__(self):
        self.next_scene = None

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass