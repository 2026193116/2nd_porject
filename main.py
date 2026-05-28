"""
메인 엔트리포인트: 이벤트 루프 및 모듈 연결 (시작화면 & 선택화면 추가 버전)
"""

import pygame
import sys
import os

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from audio import AudioManager
from entities import GameState, WordSpawner
from game_logic import process_shout, try_submit_word, update_words, spawn_word_if_ready
from renderer import Renderer

# 이미지 폴더 경로 설정 (assets)
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("보스를 향해 소리쳐! - 가로형 디펜스 에디션")

    clock = pygame.time.Clock()
    renderer = Renderer(screen)
    audio = AudioManager()
    audio.start()

    state = GameState()
    spawner = WordSpawner()
    last_spawn_time = pygame.time.get_ticks()

    # 💡 이미지 로드 (경로가 없어도 튕기지 않게 에러 처리)
    try:
        start_img = pygame.image.load(os.path.join(ASSETS_DIR, 'start_screen.png')).convert()
        setup_img = pygame.image.load(os.path.join(ASSETS_DIR, 'setup_screen.png')).convert()
        # 창 크기(1000x600)에 맞게 이미지 강제 조절
        start_img = pygame.transform.scale(start_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        setup_img = pygame.transform.scale(setup_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error:
        print("⚠️ assets 폴더 안에 start_screen.png 또는 setup_screen.png 파일이 없습니다!")
        # 이미지가 없으면 임시로 쓸 검은 화면 생성
        start_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        start_img.fill((30, 30, 30))
        setup_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        setup_img.fill((50, 50, 50))

    # 💡 '시작하기' 버튼 인식 영역 (x, y, 가로, 세로)
    # 이미지 해상도(1000x600) 기준 하단 파란 버튼 위치로 대략 맞췄습니다.
    start_button_rect = pygame.Rect(350, 350, 400, 110)

    # 💡 게임 상태 관리 변수 ("TITLE" -> "SETUP" -> "PLAY")
    game_state = "TITLE"

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        # 1. 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # ESC 누르면 언제든 즉시 종료
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                
                # 💡 [선택화면 상태] 아무 키나 누르면 게임 플레이 시작
                if game_state == "SETUP":
                    game_state = "PLAY"
                    last_spawn_time = pygame.time.get_ticks() # 시간 초기화
                    break

                # [게임 진행 중 상태]의 키 입력 분기
                if game_state == "PLAY" and not state.game_over:
                    if event.key == pygame.K_BACKSPACE:
                        state.backspace_input()
                    elif event.key == pygame.K_RETURN:
                        try_submit_word(state, current_time)
                    elif event.key == pygame.K_SPACE:
                        state.append_input(" ")
                    else:
                        if event.unicode.isalpha():
                            state.append_input(event.unicode)

            # 💡 [시작화면 상태] 마우스 클릭으로 버튼 인식
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "TITLE" and event.button == 1:
                    if start_button_rect.collidepoint(event.pos):
                        game_state = "SETUP"

        # 2. 업데이트 및 그리기 분기
        if game_state == "TITLE":
            screen.blit(start_img, (0, 0))
            pygame.display.flip()

        elif game_state == "SETUP":
            screen.blit(setup_img, (0, 0))
            
            # 선택 화면 하단에 띄울 안내 자막 (선택 사항)
            font = pygame.font.SysFont("Arial", 24)
            text_surface = font.render("Press ANY KEY to Start Game", True, (255, 255, 255))
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 50))
            pygame.display.flip()

        elif game_state == "PLAY":
            # 원래 잘 돌아가던 정석 로직 그대로 실행!
            if not state.game_over:
                process_shout(state, audio)

                last_spawn_time = spawn_word_if_ready(
                    state, spawner, current_time, last_spawn_time
                )

                update_words(state, current_time)

            # 렌더링 함수도 원래 이름인 draw_frame으로 정상 복구
            renderer.draw_frame(state, audio.get_volume(), audio.is_shouting(), current_time)
            clock.tick(FPS)

    audio.stop()
    pygame.quit()

if __name__ == "__main__":
    main()