# #####################################
# Class Name:   StatsManager
# Course:       ICS4U 
# Author:       Youngwook Go 
# Date:         2026-03-01
# File Name:    statistic.py 
# Description:  
#   This class stores and manages game statistics using a JSON file.
#    - Save important game data (ex: total games, high score) so it persists after closing the game.
#    - Keep the program stable even if the file is missing or corrupted.
#    - Provide simple methods to read and update stats/achievements.
##############################################
import json
import os

class StatsManager:
    """
    To store and manage game statistics:
    1. At startup, the manager loads data from a JSON file.
    2. If the file does not exist, it creates a new file with default values.
    3. If the file is corrupted, it resets to defaults and saves a clean file.
    """
    def __init__(self, filepath="Game/game_stats.json"):
        """
        Initialize the StatsManager object.
        - Use a default data structure so the game always has valid stats.
        - Immediately load() so the latest saved data is available right away.
        """
        self.filepath = filepath
        # Default data ensures the program always has valid keys and values.
        self.data = self.__create_default_data()
        # Load saved stats at startup.
        self.load()
    #end __init__()

    def __create_default_data(self):
        """
        Private instance method to create a default data structure.
        """
        return {
            "stats": {
                "total_games": 0,
            },
            "achievements": {
                "high_score": 0,
            }
        }
    #end __create_default_data()

    def load(self):
        """
        Load stats data from the JSON file.
        If the file is corrupted, reset to default data and save a clean file.
        """
        # If the file is missing, create the folder and save default data.
        if not os.path.exists(self.filepath):
            self.__check_folder()
            self.save()
            return

        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                loaded = json.load(file)

                # Validate that loaded data is a dictionary.
                if not isinstance(loaded, dict):
                    print("StatsManager ERROR: JSON file has unexpected format. Resetting data.")
                    self.data = self.__create_default_data()
                    self.save()
                    return

                # Merge stats section if it is valid.
                stats = loaded.get("stats", {})
                if isinstance(stats, dict):
                    self.data["stats"].update(stats)

                # Merge achievements section if it is valid.
                achievements = loaded.get("achievements", {})
                if isinstance(achievements, dict):
                    self.data["achievements"].update(achievements)

        except (json.JSONDecodeError, OSError) as error:
            # JSONDecodeError: invalid/corrupted JSON
            # OSError: file permission errors, disk errors, etc.
            print(f"StatsManager ERROR: Failed to load file -> {error}")
            self.data = self.__create_default_data()
            self.save()
    #end load()

    def save(self):
        """
        Save the current stats data to the JSON file.
        """
        self.__check_folder()
        try:
            with open(self.filepath, "w", encoding="utf-8") as file:
                json.dump(self.data, file, ensure_ascii=False, indent=2)
        except OSError as error:
            # If saving fails, the game should still run.
            print(f"StatsManager ERROR: Failed to save file -> {error}")
    #end save()

    def __check_folder(self):
        """
        Ensure the folder for the filepath exists.
        """
        folder = os.path.dirname(self.filepath)
        if folder:
            os.makedirs(folder, exist_ok=True)
    #end __check_folder()

    def get_stat(self, key):
        """
        Get a stat value safely. 
        """
        # Use .get() to avoid KeyError if the key is missing.
        # Return stat value, or 0 if the key does not exist
        return int(self.data["stats"].get(key, 0))
    #end get_stat()

    def get_achievement(self, key):
        """
        Get an achievement value safely.
        """
        # Return achievement value, or 0 if the key does not exist
        return int(self.data["achievements"].get(key, 0))
    #end get_achievement()
    
    def increment_total_games(self):
        """
        Increase the total number of games played by 1.
        """
        current = self.get_stat("total_games")
        self.data["stats"]["total_games"] = current + 1
        self.save()
        # Return updated total_games value
        return self.data["stats"]["total_games"]
    #end increment_total_games()
    
    def submit_score(self, score):
        """
        Submit a score and update high score if the new score is higher.
        """
        # Convert to int to ensure consistent comparison.
        score = int(score)

        # Update high score only if new score is greater.
        if score > self.get_achievement("high_score"):
            self.data["achievements"]["high_score"] = score
            self.save()
            return True # high score updated
        return False # score did not beat the current high score
    #end submit_score()
