"""
핵심 게임 로직 모듈 (렌더링과 분리)
"""

from entities import GameState, WordSpawner, Word
from audio import AudioManager
from config import PLAYER_X, SHOUT_PUSH_BASE

def process_shout(state: GameState, audio: AudioManager):
    """
    소리치기 처리: 임계값 초과 시 heavy가 아닌 단어를 오른쪽으로 밀어냄.
    """
    if audio.is_shouting():
        push_amount = SHOUT_PUSH_BASE + state.level
        for w in state.active_words:
            if not w.is_heavy:
                w.push_back(push_amount)

def try_submit_word(state: GameState, current_time: int) -> bool:
    """
    현재 입력을 제출하여 일치하는 단어를 제거.
    일치하면 True, 아니면 False 반환.
    """
    matched = False
    for w in state.active_words[:]:
        if w.matches(state.current_input):
            state.active_words.remove(w)
            state.add_score(100)
            state.check_level_up(current_time)
            matched = True
            break
    state.clear_input()
    return matched

def update_words(state: GameState, current_time: int):
    """
    모든 활성 단어를 이동시키고, 방어선에 닿은 단어를 처리.
    """
    for w in state.active_words[:]:
        w.update(current_time)
        if w.has_reached(PLAYER_X):
            state.lose_life()
            state.active_words.remove(w)

def spawn_word_if_ready(state: GameState, spawner: WordSpawner,
                        current_time: int, last_spawn_time: int) -> int:
    """
    스폰 딜레이가 경과했으면 새 단어 생성.
    업데이트된 last_spawn_time을 반환.
    """
    delay = spawner.get_spawn_delay(state.level)
    if current_time - last_spawn_time > delay:
        word = spawner.spawn(state.level,state.active_words)
        state.active_words.append(word)
        return current_time
    return last_spawn_time
