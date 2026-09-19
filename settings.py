"""Global settings and tuning constants for OS Quest: Survivor."""

# ---- Screen ----
SCREEN_W = 960
SCREEN_H = 600
FPS = 60
TITLE = "OS Quest: Survivor"

# ---- World (larger than the screen; camera follows the player) ----
WORLD_W = 1920
WORLD_H = 1200

# The floor occupies the lower portion of the world.
# "Sky" (above FLOOR_Y) is where quiz questions / answer buttons appear.
FLOOR_Y = int(WORLD_H * 0.5)   # top edge of the floor band

# During combat, all entities are confined to this floor band.
PLAY_FLOOR_TOP = FLOOR_Y + 24
PLAY_FLOOR_BOT = WORLD_H - 40

# Quiz "room" in the sky: where answer pads live during a quiz.
QUIZ_PAD_Y = FLOOR_Y - 250          # world-y of the answer pads
QUIZ_ROOM_TOP = QUIZ_PAD_Y - 120
QUIZ_ROOM_BOT = FLOOR_Y

# ---- Colors ----
BLACK = (12, 14, 22)
WHITE = (236, 240, 245)
DIM = (148, 163, 184)
SKY_TOP = (15, 23, 42)
SKY_BOT = (30, 27, 75)
FLOOR_TOP = (51, 65, 85)
FLOOR_BOT = (30, 41, 59)
PRIMARY = (99, 102, 241)
PRIMARY_DK = (79, 70, 229)
GREEN = (34, 197, 94)
RED = (239, 68, 68)
YELLOW = (250, 204, 21)
CYAN = (34, 211, 238)
ORANGE = (249, 115, 22)
PURPLE = (168, 85, 247)

# ---- Player defaults ----
PLAYER_BASE_SPEED = 3.6
PLAYER_BASE_HP = 100
PLAYER_BASE_DAMAGE = 10
PLAYER_BASE_FIRE_RATE = 0.55      # seconds between auto-attacks
PLAYER_BASE_RANGE = 320           # auto-attack targeting range
PLAYER_ATTACK_SPEED = 8.0         # projectile speed
PLAYER_PICKUP_RANGE = 42          # how close to a button counts as "near"

# ---- Enemy tuning ----
ENEMY_BASE_HP = 20
ENEMY_BASE_SPEED = 1.3
ENEMY_TOUCH_DAMAGE = 8            # per second while touching player

# ---- Stage / wave structure ----
NUM_STAGES = 5
WAVES_PER_STAGE = 3               # ~3 waves, then a quiz
CODE_SNIPPET_WAVE = 5            # from this stage on, code-snippet questions appear
