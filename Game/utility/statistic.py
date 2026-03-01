import json
import os

class StatsManager:
    def __init__(self, filepath="Game/game_stats.json"):
        self.filepath = filepath
        self.data = {
            "stats": {
                "total_games": 0,
            },
            "achievements": {
                "high_score": 0,
            }
        }
        self.load()

    # File management ---------------------------
    def load(self):
        if not os.path.exists(self.filepath):
            self._ensure_folder()
            self.save()
            return

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    stats = loaded.get("stats", {})
                    achievements = loaded.get("achievements", {})
                    if isinstance(stats, dict):
                        self.data["stats"].update(stats)
                    if isinstance(achievements, dict):
                        self.data["achievements"].update(achievements)
        except (json.JSONDecodeError, OSError):
            self.data = {
                "stats": {
                    "total_games": 0,
                },
                "achievements": {
                    "high_score": 0,
                }
            }
            self.save()

    def save(self):
        self._ensure_folder()
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def _ensure_folder(self):
        folder = os.path.dirname(self.filepath)
        if folder:
            os.makedirs(folder, exist_ok=True)

    # ====================================================================

    # Get stats & achieves ----------------------
    def get_stat(self, key: str) -> int:
        return int(self.data["stats"].get(key, 0))

    def get_achievement(self, key: str) -> int:
        return int(self.data["achievements"].get(key, 0))
    
    # Manage stats ------------------------------
    def increment_total_games(self) -> int:
        """Manage total_games stat"""
        self.data["stats"]["total_games"] = self.get_stat("total_games") + 1
        self.save()
        return self.data["stats"]["total_games"]
    
    # Manage acheives ---------------------------
    def submit_score(self, score: int) -> bool:
        """Manage high_score stat"""
        score = int(score)
        if score > self.get_achievement("high_score"):
            self.data["achievements"]["high_score"] = score
            self.save()
            return True
        return False
