import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from audio import AudioManager
from entities import GameState, WordSpawner
from game_logic import process_shout, try_submit_word, update_words, spawn_word_if_ready
from renderer import Renderer
# ----------------- [추가: 시작 메뉴 모듈 불러오기] -----------------
from start_menu import show_start_menu
# -----------------------------------------------------------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("보스를 향해 소리쳐! - 가로형 디펜스 에디션")

    # ----------------- [추가: 게임 루프 진입 전 시작화면 띄우기] -----------------
    # 화면(screen)을 넘겨주고 사용자가 버튼을 누를 때까지 여기서 대기합니다.
    show_start_menu(screen)
    # -------------------------------------------------------------------------

    clock = pygame.time.Clock()
    renderer = Renderer(screen)
    audio = AudioManager()
    audio.start()

    state = GameState()
    spawner = WordSpawner()
    last_spawn_time = pygame.time.get_ticks()

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                
                if not state.game_over:
                    if event.key == pygame.K_BACKSPACE:
                        state.backspace_input()
                    elif event.key == pygame.K_RETURN:
                        try_submit_word(state, current_time)
                    elif event.key == pygame.K_SPACE:
                        state.append_input(" ")
                    else:
                        if event.unicode.isalpha():
                            state.append_input(event.unicode)

        if not state.game_over:
            process_shout(state, audio, current_time)
            last_spawn_time = spawn_word_if_ready(
                state, spawner, current_time, last_spawn_time
            )
            update_words(state, current_time)

        renderer.draw_frame(state, audio.get_volume(),
                            audio.is_shouting(), current_time)
        clock.tick(FPS)

    audio.stop()
    pygame.quit()

if __name__ == "__main__":
    main()