"""
핵심 게임 로직 모듈 (3초 쿨타임 및 밀어내기 조건 수정)
"""

from entities import GameState, WordSpawner, Word
from audio import AudioManager
from config import PLAYER_X, SHOUT_PUSH_BASE, SHOUT_PUSH_LEVEL_BONUS, SHOUT_COOLDOWN

def process_shout(state: GameState, audio: AudioManager, current_time: int):
    """
    [수정 완료] 인자 3개(current_time 추가)를 정상적으로 받도록 수정되었습니다.
    85dB 이상 소리치기 처리 및 3초 쿨타임 로직 구현
    """
    is_now_shouting = audio.is_shouting()

    # 1. 현재 쿨타임 상태 업데이트 계산
    if state.is_cooling_down:
        if current_time - state.last_shout_success_time > SHOUT_COOLDOWN:
            state.is_cooling_down = False  # 3초가 지나면 쿨타임 해제

    # 2. 소리를 지르고 있고, 쿨타임이 아닐 때만 밀어내기 작동
    if is_now_shouting and not state.is_cooling_down:
        push_amount = SHOUT_PUSH_BASE + (state.level * SHOUT_PUSH_LEVEL_BONUS)
        for w in state.active_words:
            if not w.is_heavy:
                w.push_back(push_amount)
        
        # 소리 지르기 유지 중인 상태 기록
        state.was_shouting_last_frame = True
    else:
        # 소리를 지르고 있다가 방금 멈췄을 때 -> 3초 쿨타임 가동시작!
        if state.was_shouting_last_frame and not is_now_shouting:
            state.last_shout_success_time = current_time
            state.is_cooling_down = True
        state.was_shouting_last_frame = False


def try_submit_word(state: GameState, current_time: int) -> bool:
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
    for w in state.active_words[:]:
        w.update(current_time)
        if w.has_reached(PLAYER_X):
            state.lose_life()
            state.active_words.remove(w)


def spawn_word_if_ready(state: GameState, spawner: WordSpawner,
                        current_time: int, last_spawn_time: int) -> int:
    delay = spawner.get_spawn_delay(state.level)
    if current_time - last_spawn_time > delay:
        # 중복 방지를 위해 state.active_words 인자 전달
        word = spawner.spawn(state.level, state.active_words)
        state.active_words.append(word)
        return current_time
    return last_spawn_time