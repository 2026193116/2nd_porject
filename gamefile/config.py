"""
게임 전역 설정값 (상수) - 85dB 및 3초 쿨타임 완벽 반영 버전
"""

# 화면
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 0)
PURPLE = (200, 50, 255)
CYAN = (50, 255, 255)

# 게임 밸런스
INITIAL_LIVES = 3
INITIAL_LEVEL = 1
INITIAL_NEXT_LEVEL_TARGET = 10
LEVEL_UP_DISPLAY_DURATION = 2000  # ms
MAX_LEVEL = 5                     # ⭐ 최대 레벨 5으로 제한

# ⭐ 오디오 및 소리치기 설정 (여기가 들어가 있어야 에러가 안 납니다!)
DB_THRESHOLD = 85.0              # 85dB 이상일 때만 인식
SHOUT_COOLDOWN = 3000            # 소리치기 후 쿨타임 3초 (ms)

# 위치
BOSS_X = SCREEN_WIDTH - 80
BOSS_Y = SCREEN_HEIGHT // 2
PLAYER_X = 50

# 단어 스폰
SPAWN_DELAY_BASE = 2000
SPAWN_DELAY_MIN = 600
SPAWN_DELAY_LEVEL_REDUCTION = 200

# 레인 시스템
Y_LANES = [100, 160, 220, 280, 340, 400, 460, 520]
MAX_RECENT_LANES = 3

# 단어 풀
WORD_POOL = [
    "APPLE", "BANANA", "CODE", "PYTHON", "GAME", "BOSS", "ATTACK",
    "SHOUT", "VOICE", "MATRIX", "DANGER", "ESCAPE", "I AM THE BOSS",
    "NEVER GIVE UP", "KEYBOARD", "DEFENSE"
]

# 무거운 단어 확률
HEAVY_CHANCE_BASE = 0.1
HEAVY_CHANCE_PER_LEVEL = 0.05
HEAVY_CHANCE_MAX = 0.6

# 단어 속도 설정 (400타 제한 및 레벨별 증가 반영)
WORD_SPEED_MIN = 0.8
WORD_SPEED_MAX = 1.8
WORD_SPEED_LEVEL_BONUS = 0.25   # 레벨마다 속도가 점점 빨라짐
WORD_SPEED_LIMIT = 3.5          # 400타 수준을 넘어가지 않도록 하는 최대 프레임당 속도 상한선

# 단어 진폭/주파수 범위
WORD_AMP_MIN = 15
WORD_AMP_MAX = 40
WORD_FREQ_MIN = 200.0
WORD_FREQ_MAX = 600.0

# 소리치기 밀어내기
SHOUT_PUSH_BASE = 6
SHOUT_PUSH_LEVEL_BONUS = 1