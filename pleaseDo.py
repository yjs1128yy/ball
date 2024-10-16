from asyncio.windows_events import NULL
import pygame
import math
import random

screen_width = 600
screen_height = 750

skwed_probabitity = [0.7, 0.1, 0.05, 0.08, 0.04, 0.02, 0.01, 0, 0]

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
orange = (255,165,0)
yellow = (255,255,0)
green  = (0 , 255 , 0)
blue = (0,0,255)
thistle = (255, 0, 255)
hot_pink = (255, 105, 180)
purple = (128, 0, 128)

color_order = [white, red, orange,yellow, green, blue, thistle, hot_pink, purple]

screen = pygame.display.set_mode((screen_width, screen_height))

# 공 점수 정의
white_score = 0
red_score = 2
orange_score = 4
yellow_score = 8
green_score = 8
blue_score = 16
thistle_score = 32
hot_pink_score = 64
purple_score = 128

score = 0
score_order = [white_score, red_score, orange_score, yellow_score, green_score, blue_score, thistle_score, hot_pink_score, purple_score]

# 공 속도 반지름 정의
ball_speed = 1
white_radius = 15
red_radius = 22
orange_radius = 42
yellow_radius = 55
green_radius = 68
blue_radius = 85
thistle_radius = 94
hot_pink_radius = 110
purple_radius = 130

radius_order = [white_radius, red_radius, orange_radius, yellow_radius, green_radius, blue_radius, thistle_radius, hot_pink_radius, purple_radius]

gravity = 0.05

balls = []
balls_to_add = []
balls_to_remove = []

pygame.init()
running = True
gaem_over = False

index = range(len(color_order))
random_int = random.choices(index, weights=skwed_probabitity, k=1)[0]
next_ball_radius = radius_order[random_int]
next_ball_color = color_order[random_int]
n_next_ball_color = NULL
n_next_index = random.choices(index, weights=skwed_probabitity, k=1)[0]

while running:

    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] > 40 and event.pos[0]<560 and event.pos[1]< 40:
                # 마우스 클릭시 공 생성
                ball_x = event.pos[0]
                ball_y = event.pos[1]
                horizontal_speed = 0 
                is_dropping = True
                balls.append([ball_x, ball_y, ball_speed, horizontal_speed, next_ball_color, next_ball_radius, is_dropping])
                next_index = n_next_index
                n_next_index = random.choices(index, weights=skwed_probabitity, k=1)[0]
                next_ball_color = color_order[next_index]
                next_ball_radius = radius_order[next_index]
                n_next_ball_color = color_order[n_next_index]
    
        elif event.type == pygame.MOUSEMOTION and event.pos[0] > 40 and event.pos[0]<560 and event.pos[1]< 40:
            # 다음 공 생성
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
            pygame.draw.circle(screen, next_ball_color, (mouse_x, mouse_y), next_ball_radius)
            
    if not gaem_over:
        for i in range(len(balls)):
            for j in range(i+1, len(balls)):
                dx = balls[i][0] - balls[j][0]
                dy = balls[i][1] - balls[j][1]

                distance = math.sqrt(dx **2 + dy **2)
                if distance < balls[i][5] + balls[j][5]:
                    # 같은 공인지 판단
                    if balls[i][4] == balls[j][4]:
                        color_index = color_order.index(balls[i][4])
                        # 마지막  공이 충돌하면 공 제거후 점수 두 배
                        if color_index == len(color_order) - 1:
                            score += score_order[color_index] * 2
                        if color_index + 1 < len(color_order):
                            # 다음 색인 공 만들기
                            # 충돌 후 수평 속도의 합
                            new_x = (balls[i][0] + balls[j][0]) / 2 + random.uniform(-1,1)
                            new_y = (balls[i][1] + balls[j][1]) / 2 + random.uniform(0,1)
                            balls_to_add.append([new_x, new_y, balls[i][2] , balls[i][3] + balls[j][3],  color_order[color_index + 1], radius_order[color_index + 1], False])
                            # 점수 업데이트
                            score += score_order[color_index + 1]
                        # 원래 공 제거
                        balls_to_remove.append(balls[i])
                        balls_to_remove.append(balls[j])
                        break
                    # 색상이 같지 않은 경우
                    else:
                        # 중복 확인
                        overlap = balls[i][5] + balls[j][5] - distance
                        dx = dx / distance
                        dy = dy / distance
                        balls[i][0] += dx * overlap / 2
                        balls[i][1] += dy * overlap / 2
                        balls[j][0] -= dx * overlap / 2
                        balls[j][1] -= dy * overlap / 2

                        # 충돌시 두 공의 속도를 업데이트
                        balls[i][2] = 0 
                        balls[j][2] = 0
                        balls[i][3] *= 1
                        balls[j][3] *= 1

                        # is_dropping 업데이트
                        balls[i][6] = False
                        balls[j][6] = False

        # 공 제거 추가
        for ball in balls_to_remove:
            if ball in balls:
                balls.remove(ball)
        for ball in balls_to_add:
            balls.append(ball)
        # 리스트 비우기
        balls_to_remove.clear()
        balls_to_add.clear()
        # 공 그리기
        for ball in balls:
            box_top = 40
            # 공이 선 위에서 충돌하면 게임 종료
            if (not ball[6]) and ball[1] - ball[5] < box_top:
                gaem_over = True
                break
            ball[2] += gravity

            box_bottom = 720 - ball[5]
            box_left = 40 + ball[5]
            box_right = 560 - ball[5]
            if ball[1] >= box_bottom:
                ball[1] = box_bottom
            elif ball[1] < box_bottom:
                ball[1] += ball[2]
            
            # 공 x 위치 업데이트
            ball[0] += ball[3]
            # 공이 x에서 상자 밖에 있는지 확인
            if ball[0] < box_left:
                ball[0] = box_left + 1
                ball[3] *= -0.5
            elif ball[0] > box_right:
                ball[0] = box_right - 1
                ball[3] *= -0.5
            any_ball = pygame.draw.circle(screen, ball[4], (ball[0], ball[1]), ball[5])
        # 상자 그리기
        pygame.draw.line(screen, white, (40, 40), (40, 720), 1)
        pygame.draw.line(screen, white, (40, 720), (560, 720), 1)
        pygame.draw.line(screen, white, (560, 720), (560, 40), 1)
        # 점선 그리기
        dotted_line_y = 40
        dotted_line_length = 4
        dotted_line_space = 4
        dotted_line_color = (128,128,128)
        for x in range(40, 560, dotted_line_length + dotted_line_space):
            pygame.draw.line(screen, dotted_line_color, (x, dotted_line_y), (x + dotted_line_length, dotted_line_y), 1)
        
        # 색 순서와 다음 색 그리기
        color_order_y = screen_height - 20  
        color_order_spacing = 40  
        for i, color in enumerate(color_order):
            pygame.draw.circle(screen, color, (40 + i * color_order_spacing, color_order_y), 10)
        pygame.draw.circle(screen, n_next_ball_color, (550, screen_height - 20), 10)

        # 텍스트 그리기
        font = pygame.font.Font(None, 36)
        nfont = pygame.font.Font(None, 25)
        score_text = font.render(f'Score: {score}', True, white)
        screen.blit(score_text, (screen_width /2 - score_text.get_width()/2, 20))
        text = nfont.render(f'Next Ball:', True, white)
        screen.blit(text, (450, screen_height - 27))
        pygame.display.update()

        

    if gaem_over:
        font = pygame.font.Font(None, 36)
        game_over_text_lines = [
            "GAME OVER",
            f"Your Score is: {score}",
            "restart by pressing SPACE",
            "quit game by pressing ESCAPE"
        ]
        for i, line in enumerate(game_over_text_lines):
            line_text = font.render(line, True, white)
            screen.blit(line_text, (screen_width / 2 - line_text.get_width() / 2, screen_height / 2 - line_text.get_height() / 2 + i * line_text.get_height()))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # space 누르면 리셋
                    balls.clear()
                    balls_to_add.clear()
                    balls_to_remove.clear()
                    score = 0
                    gaem_over = False
                elif event.key == pygame.K_ESCAPE:
                    # esc 누르면 종료
                    running = False

pygame.quit()
