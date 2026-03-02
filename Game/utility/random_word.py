# #####################################
# Class Name:   RandomWord
# Course:       ICS4U 
# Author:       Youngwook Go 
# Date:         2026-03-01
# File Name:    random_word.py 
##############################################
import requests

class RandomWord:
    """
    This class provides random words to use in the game. 
    To do so:
    - Retrieves set of random words from an external API.
    - Stores them in an internal buffer.
    - Provides words sequentially.
    """
    # Constant URL for the external random word API.
    __API_URL = "https://random-word-api.herokuapp.com/word"

    def __init__(self, prefetch=50, refill_at=10, timeout=5):
        """
        Initialize a new RandomWord instance.
        """
        # Validate prefetch value.
        if not isinstance(prefetch, int) or prefetch <= 0:
            prefetch = 50

        # Validate refill threshold.
        if not isinstance(refill_at, int) or refill_at < 0:
            refill_at = 10

        # Validate timeout value.
        if not isinstance(timeout, int) or timeout <= 0:
            timeout = 5

        # Number of words to request per API call.
        self.prefetch = prefetch

        # Threshold for automatic refill.
        # When buffer size <= refill_at, automatically refill
        self.refill_at = refill_at

        # Timeout in seconds for API requests.
        self.timeout = timeout

        # Internal buffer storing prefetched words.
        self.buffer = []

        # Fallback words used if the API fails.
        self.offline_words = [
            "computer", "science", "typing", "practice", "game",
            "statistic", "random", "requirements", "assignment", "final",
            "library", "journey", "respect", "balance", "success",
            "entrepreneur", "conscientious", "meticulous", "phenomenon", "extraordinary",
        ]

        # Prefill at startup so the first word is available immediately.
        self.refill()
    #end __init__()

    def refill(self):
        """
        Downloads a list of words by calling the API and stores them in a buffer.
        If the API fails and the buffer is empty, fallback words are added so the game can continue.
        """
        try:
            api_url = RandomWord.get_api_url()
            response = requests.get(
                api_url,
                params={"number": self.prefetch},
                timeout=self.timeout
            )
            
            # Raise error for bad HTTP status codes.
            response.raise_for_status()

            words = response.json()

            # Ensure the API response is a list.
            if not isinstance(words, list):
                print("RandomWord ERROR: API returned unexpected JSON format.")
                self.__offline_words()
                return

            # Store clean, non-empty words.
            added = 0
            for w in words:
                if isinstance(w, str):
                    word = w.strip()
                    if word:  # ignore empty strings
                        self.buffer.append(word)
                        added += 1

            # If API returned no valid words.
            if added == 0:
                print("RandomWord ERROR: No valid words received.")
                self.__offline_words()

        except requests.RequestException as error:
            # Network error (timeout, connection issue, etc.)
            print(f"RandomWord ERROR: API request failed -> {error}")
            self.__offline_words()

        except ValueError as error:
            # JSON parsing error.
            print(f"RandomWord ERROR: Invalid JSON response -> {error}")
            self.__offline_words()
    #end refill() 

    def get_word(self):
        """
        Return one word from the buffer and refills automatically if the buffer is low.
        """
        # Refill if buffer is running low.
        if len(self.buffer) <= self.refill_at:
            self.refill()

        # Return the next word in order.
        if self.buffer:
            return self.buffer.pop(0)

        return None
    #end get_word()

    def __offline_words(self):
        """
        Internal class method:
            Use fallback words only if the buffer is empty.
            This prevents the game from stopping due to internet/API issues.
        """
        if not self.buffer:
            self.buffer.extend(self.offline_words)
    #end offline_words()

    @classmethod
    def get_api_url(cls):
        """
        Return the API URL to get random word list.
        """
        return cls.__API_URL
    #end get_api_url()
