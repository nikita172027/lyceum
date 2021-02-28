import pygame
from random import randrange as rnd
import sys
import PyQt5
from PyQt5 import uic
import time
from PyQt5.QtCore import QTimer, QUrl, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton 
from PyQt5.QtWidgets import QLabel, QLineEdit, QMainWindow, QListWidget
from PyQt5.QtGui import QIntValidator


class QMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)
        self.button_play.clicked.connect(self.button_play_click)
        
    def button_play_click(self):
        gameingame()

    
def gameingame():
    WIDTH, HEIGHT = 1200, 800
    fps = 60
    paddle_w = 330
    paddle_h = 35
    paddle_speed = 15
    paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)
    ball_radius = 20
    ball_speed = 8
    ball_rect = int(ball_radius * 2 ** 0.5)
    ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
    dx, dy = 1, -1
    block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
    color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]
    pygame.init()
    pygame.display.set_caption('ИГРА, БЛОКИ')
    sc = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    img = pygame.image.load('1.jpg').convert()
    time.sleep(1)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        if ball.bottom > HEIGHT:
            pygame.display.set_caption('LOSE!')
            exit()
        elif not len(block_list):
            pygame.display.set_caption('WIN!')
            exit()        
        sc.blit(img, (0, 0))
        [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
        pygame.draw.rect(sc, pygame.Color('orange'), paddle)
        pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)
        ball.x += ball_speed * dx
        ball.y += ball_speed * dy
        if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
            dx = -dx
        if ball.centery < ball_radius:
            dy = -dy
        if ball.colliderect(paddle) and dy > 0:
            dx, dy = detect_collision(dx, dy, ball, paddle)
        hit_index = ball.collidelist(block_list)
        if hit_index != -1:
            hit_rect = block_list.pop(hit_index)
            hit_color = color_list.pop(hit_index)
            dx, dy = detect_collision(dx, dy, ball, hit_rect)
            pygame.draw.rect(sc, hit_color, hit_rect)
        if ball.bottom > HEIGHT:
            pygame.display.set_caption('LOSE!')
            exit()
        elif not len(block_list):
            pygame.display.set_caption('WIN!')
            exit()
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddle_speed
        if key[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.right += paddle_speed
        pygame.display.flip()
        clock.tick(fps)    


def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        x_cord = ball.right - rect.left
    else:
        x_cord = rect.right - ball.left
    if dy > 0:
        y_cord = ball.bottom - rect.top
    else:
        y_cord = rect.bottom - ball.top

    if abs(x_cord - y_cord) < 10:
        dx, dy = -dx, -dy
    elif x_cord > y_cord:
        dy = -dy
    elif y_cord > x_cord:
        dx = -dx
    return dx, dy
    
if __name__ == "__main__": # Запуск программы
    app = QApplication(sys.argv)
    ex = QMainWindow()
    ex.show()
    sys.exit(app.exec_())   