import cv2
import time
import cv2.videoio_registry
import pygame.locals
import requests
import pygame
from pyzbar.pyzbar import decode
from pygame.locals import QUIT,KEYDOWN,K_ESCAPE

#カメラの宣言と初期化
def initializeCamera():
    cam = cv2.VideoCapture(0)
    return cam

#ウィンドウの作成
def initializeWindow(width,height):
    pygame.init()
    frame = pygame.display.set_mode((width,height))
    pygame.display.set_caption('UbiClient')
    return frame



def main():
    cam = initializeCamera()
    window = initializeWindow(960,720)

    running = True
    
    #以下メインループ
    while running:
        ret, frame = cam.read()
        
    cam.release()
    pygame.quit()
    #メインループ終了

if __name__ == "__main__":
    main()

