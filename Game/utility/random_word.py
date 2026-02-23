import requests

class RandomWord:
    """
    Fetch a random english word from online API.
    """

    API_URL = "https://random-word-api.herokuapp.com/canada"

    def __init__(self):
        pass

    def get_word(self):
        try:
            response = requests.get(self.API_URL, timeout=5)

            data = response.json()
            return data[0] if data else None

        except Exception as e:
            print("RandomWord ERROR:", repr(e))
            return None
