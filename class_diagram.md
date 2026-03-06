class Game {
    +WIDTH: int
    +HEIGHT: int
    +FPS: int
    +scene: Scene
    +run() None
    +manage_scene() None
    +quit() None
}

class Scene {
    +request_scene: str|None
    +request_quit: bool
    +manage_event(events: list[Event]) None
    +update() None
    +draw(screen: Surface) None
}

class MenuScene {
    +status: str
    +manage_event(events: list[Event]) None
    +draw(screen: Surface) None
}

class GameScene {
    +score: int
    +combo: int
    +stage: int
    +energy: int
    +paused: bool
    +spawn_enemy(y: float) Enemy
    +check_input() None
    +skill1() None
    +defeat_enemy(enemy: Enemy) None
    +game_over() None
    +set_paused(paused: bool) None
}

class Button {
    +locate(x: int, y: int) None
    +interact(event: Event) bool
    +draw(screen: Surface) None
}

class IconButton

class TextBox {
    +text: str
    +active: bool
    +locate(x: int, y: int) None
    +clear() None
    +get_text() str
    +update(dt: float) None
    +interact(event: Event) None
    +draw(screen: Surface) None
}

class RandomWord {
    +prefetch: int
    +refill_at: int
    +timeout: float
    +buffer: list[str]
    +refill() None
    +get_word() str
    +get_api_url() str
}

class StatsManager {
    +filepath: str
    +data: dict[str, Any]
    +load() None
    +save() None
    +get_stat(key: str) int|float|str|bool|None
    +get_achievement(key: str) bool
    +increment_total_games() None
    +submit_score(score: int) None
}

class OverlayMenu {
    +handle_event(event: Event) bool
    +draw(screen: Surface) None
}

class PauseOverlayMenu
class GuideOverlayMenu

class OverlayMenuManager {
    +register(name: str, menu: OverlayMenu) None
    +open(name: str) None
    +close() None
    +is_open() bool
    +handle_event(event: Event) bool
    +draw(screen: Surface) None
}

class Enemy {
    +word: str
    +durability: int
    +speed: float
    +passed: bool
    +new_word() str
    +take_damage() bool
    +damage_effect() None
    +exit_effect(scene: GameScene) None
    +calculate_speed() float
    +update(dt: float) None
}

class Enemy1
class Enemy2 {
    +ENERGY_REWARD: int
    +exit_effect(scene: GameScene) None
}
class Enemy3 {
    +DURABILITY_REWARD: int
    +take_damage() bool
    +exit_effect(scene: GameScene) None
}

Scene <|-- MenuScene
Scene <|-- GameScene
Button <|-- IconButton
OverlayMenu <|-- PauseOverlayMenu
OverlayMenu <|-- GuideOverlayMenu
Enemy <|-- Enemy1
Enemy <|-- Enemy2
Enemy <|-- Enemy3

Game o-- Scene : current scene
Game ..> MenuScene : creates
Game ..> GameScene : creates

Scene o-- Button : quit/start/guide

MenuScene o-- OverlayMenuManager
MenuScene ..> GuideOverlayMenu

GameScene o-- RandomWord
GameScene o-- StatsManager
GameScene o-- TextBox
GameScene o-- IconButton
GameScene o-- OverlayMenuManager
GameScene o-- Enemy : sprite group
GameScene ..> PauseOverlayMenu
GameScene ..> GuideOverlayMenu
GameScene ..> Enemy1
GameScene ..> Enemy2
GameScene ..> Enemy3

OverlayMenuManager o-- OverlayMenu
PauseOverlayMenu ..> Button
GuideOverlayMenu ..> Button