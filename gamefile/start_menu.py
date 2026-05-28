import pygame
import sys

def show_start_menu(screen):
    """
    배경과 버튼이 하나로 합쳐진 통이미지를 사용하는 시작 화면 함수.
    Figma에서 디자인한 버튼의 위치를 가상 사각형(Rect)으로 지정하여 클릭을 감지합니다.
    """
    clock = pygame.time.Clock()
    
    # 1. 배경 통이미지 로드 및 화면 크기(1000x600) 맞춤
    try:
        # assets 폴더 안에 이미지를 넣어두세요. 파일명은 자유롭게 수정 가능합니다.
        background = pygame.image.load("gamefile/start_background.png").convert()
        background = pygame.transform.scale(background, (1000, 600))
    except pygame.error:
        print("시작 화면 배경 이미지를 로드할 수 없습니다. 경로와 파일명을 확인하세요.")
        return True # 이미지 로드 실패 시 에러 방지를 위해 즉시 게임 시작 처리

    # 2. ⭐ 핵심: 이미지 내부의 버튼 위치를 사각형(Rect) 영역으로 설정
    # 형식: pygame.Rect(X좌표, Y좌표, 가로크기, 세로크기)
    # 💡 [필독] Figma에서 디자인을 보시고, 버튼 사각형의 실제 위치와 크기로 값을 수정해주세요!
    # 예시: 가로 1000 해상도 중 가운데(X=400), 아래쪽(Y=450)에 위치한 200x60 크기의 버튼 영역
    button_rect = pygame.Rect(400, 450, 200, 60)

    menu_running = True
    while menu_running:
        # 화면에 배경 통이미지 그리기
        screen.blit(background, (0, 0))
        
        # (선택 사항) 개발 중 버튼 영역이 제대로 잡혔는지 임시로 빨간 테두리를 그려 확인해볼 수 있습니다.
        # 확인이 끝나면 아래 줄 맨 앞에 #을 붙여 주석 처리하거나 지우시면 됩니다.
        # pygame.Draw.rect(screen, (255, 0, 0), button_rect, 2)
        
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                # 시작 화면에서도 ESC를 누르면 바로 창이 완전히 닫히도록 처리
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # 마우스 클릭 이벤트 감지
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # 마우스 왼쪽 버튼 클릭 시
                    mouse_pos = event.pos # 현재 클릭된 마우스 커서의 (X, Y) 좌표
                    
                    # 마우스 좌표가 통이미지 내 지정한 버튼 사각형 영역 안인지 검사
                    if button_rect.collidepoint(mouse_pos):
                        print("Figma 이미지 내 버튼 영역 클릭됨! 게임을 시작합니다.")
                        menu_running = False # 루프 탈출
                        return True # main.py로 신호를 보내 게임 루프를 시작하게 함

        pygame.display.flip()
        clock.tick(60)