"""
게임 엔티티 (단어, 플레이어 상태, 보스) 모듈 - 6레벨 제한 반영
"""

import random
import math
from config import (
    WORD_POOL, Y_LANES, MAX_RECENT_LANES, BOSS_X,
    HEAVY_CHANCE_BASE, HEAVY_CHANCE_PER_LEVEL, HEAVY_CHANCE_MAX,
    WORD_SPEED_MIN, WORD_SPEED_MAX, WORD_SPEED_LEVEL_BONUS, WORD_SPEED_LIMIT,
    WORD_AMP_MIN, WORD_AMP_MAX, WORD_FREQ_MIN, WORD_FREQ_MAX,
    INITIAL_LIVES, INITIAL_LEVEL, MAX_LEVEL, INITIAL_NEXT_LEVEL_TARGET,
    PLAYER_X, SHOUT_PUSH_BASE,
    SPAWN_DELAY_BASE, SPAWN_DELAY_MIN, SPAWN_DELAY_LEVEL_REDUCTION
)

class Word:
    def __init__(self, text: str, x: float, base_y: int,
                 amp: int, freq: float, speed: float, is_heavy: bool):
        self.text = text
        self.x = x
        self.y = float(base_y)
        self.base_y = base_y
        self.amp = amp
        self.freq = freq
        self.speed = speed
        self.is_heavy = is_heavy

    def update(self, current_time: int):
        self.x -= self.speed
        self.y = self.base_y + math.sin(current_time / self.freq * self.amp)

    def push_back(self, amount: float):
        self.x += amount

    def has_reached(self, threshold_x: float) -> bool:
        return self.x < threshold_x

    def matches(self, input_text: str) -> bool:
        return self.text == input_text.upper().strip()

    def starts_with(self, input_text: str) -> bool:
        stripped = input_text.strip()
        if not stripped:
            return False
        return self.text.startswith(stripped.upper())


class WordSpawner:
    def __init__(self, word_pool: list = None, y_lanes: list = None):
        self.word_pool = word_pool or WORD_POOL
        self.y_lanes = y_lanes or Y_LANES
        self.recent_lanes = []

    def get_spawn_delay(self, level: int) -> int:
        delay = SPAWN_DELAY_BASE - (level * SPAWN_DELAY_LEVEL_REDUCTION)
        return max(SPAWN_DELAY_MIN, delay)

    def get_heavy_chance(self, level: int) -> float:
        return min(HEAVY_CHANCE_MAX, HEAVY_CHANCE_BASE + (level * HEAVY_CHANCE_PER_LEVEL))

    def choose_lane(self) -> int:
        available = [l for l in self.y_lanes if l not in self.recent_lanes]
        if not available:
            available = self.y_lanes
        chosen = random.choice(available)
        self.recent_lanes.append(chosen)
        if len(self.recent_lanes) > MAX_RECENT_LANES:
            self.recent_lanes.pop(0)
        return chosen

    def spawn(self, level: int, active_words: list) -> Word:
        lane = self.choose_lane()
        is_heavy = random.random() < self.get_heavy_chance(level)

        current_active_texts = {w.text for w in active_words}
        available_words = [w for w in self.word_pool if w not in current_active_texts]
        
        if not available_words:
            available_words = self.word_pool
            
        chosen_text = random.choice(available_words)

        calculated_speed = random.uniform(WORD_SPEED_MIN, WORD_SPEED_MAX) + (level * WORD_SPEED_LEVEL_BONUS)
        final_speed = min(calculated_speed, WORD_SPEED_LIMIT)

        return Word(
            text=chosen_text,
            x=BOSS_X - 20,
            base_y=lane,
            amp=random.randint(WORD_AMP_MIN, WORD_AMP_MAX),
            freq=random.uniform(WORD_FREQ_MIN, WORD_FREQ_MAX),
            speed=final_speed,
            is_heavy=is_heavy
        )


class GameState:
    def __init__(self):
        self.lives = INITIAL_LIVES
        self.score = 0
        self.level = INITIAL_LEVEL
        self.words_cleared = 0
        self.next_level_target = INITIAL_NEXT_LEVEL_TARGET
        self.level_up_time = 0
        self.game_over = False
        self.current_input = ""
        self.active_words: list[Word] = []
        
        self.last_shout_success_time = 0  
        self.is_cooling_down = False      
        self.was_shouting_last_frame = False 

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True

    def add_score(self, base_score: int = 100):
        self.score += base_score * self.level
        self.words_cleared += 1

    def check_level_up(self, current_time: int) -> bool:
        """단어를 맞췄을 때 호출되며, 6레벨까지만 상승하도록 제한"""
        if self.words_cleared >= self.next_level_target:
            if self.level < MAX_LEVEL:  # ⭐ 6레벨 미만일 때만 레벨 업 진행
                self.level += 1
                self.next_level_target += 10 + (self.level * 5)
                self.level_up_time = current_time
                return True
        return False

    def append_input(self, char: str):
        self.current_input += char

    def backspace_input(self):
        self.current_input = self.current_input[:-1]

    def clear_input(self):
        self.current_input = ""