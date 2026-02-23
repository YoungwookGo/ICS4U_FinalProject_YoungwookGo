import requests

class RandomWord:
    """
    Fetch a random english word from online API.
    """

    API_URL = "https://random-word-api.herokuapp.com/word"

    def __init__(self, prefetch=50, refill_at=10):
        self.prefetch = prefetch
        self.refill_at = refill_at
        self.buffer = []
        self.refill()  # 시작 시 미리 채움

    def refill(self):
        try:
            response = requests.get(
                self.API_URL,
                params={"number": self.prefetch},
                timeout=5
            )

            response.raise_for_status()
            words = response.json()

            if isinstance(words, list):
                self.buffer.extend(words)

        except requests.RequestException as e:
            print("RandomWord ERROR:", e)


    def get_word(self):
        if len(self.buffer) <= self.refill_at:
            self.refill()

        if self.buffer:
            return self.buffer.pop(0)

        return None
