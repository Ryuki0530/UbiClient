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
    
    while running:
        #以下メインループ

        #映像取得と描画
        ret, frame = cam.read()
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.transpose(frame_rgb)
        frame_surface = pygame.surfarray.make_surface(frame_rgb)
        
        window.blit(frame_surface, (0, 0))
        pygame.display.update()
        #メインループ終了

        
    cam.release()
    pygame.quit()
    
if __name__ == "__main__":
    main()

