import cv2
import time
import cv2.videoio_registry
import pygame.locals
import requests
import pygame
from pyzbar.pyzbar import decode
from pygame.locals import QUIT,KEYDOWN,K_ESCAPE

#バックエンド接続先
BACKEND_API ='http://localhost/UbiquitousCore/ubiCoreMain.php'
#コード読み取り重複防止用の待機時間
INTERVAL = 5

#カメラの宣言と初期化
def initializeCamera():
    print("Initializing camera")
    print(".")
    print(".")
    print(".")
    cam = cv2.VideoCapture(0)
    return cam

#ウィンドウの作成
def initializeWindow(width,height):
    pygame.init()
    frame = pygame.display.set_mode((width,height))
    pygame.display.set_caption('UbiClient')
    return frame

#QRコードスキャナー
def qrScanner(frame):
    data = None
    for qr in decode(frame):
        data = qr.data.decode("utf-8")
        print("QR code confirmed.")
        return data
    return None



def main():
    cam = initializeCamera()
    window = initializeWindow(960,720)

    lastScanedTime = 0
    intervalTime = INTERVAL

    running = True
    
    while running:
        #以下メインループ
        
        currentTime = time.time()
        clock = pygame.time.Clock()

        #映像取得と描画
        ret, currentframe = cam.read()
        
        frameRgb = cv2.cvtColor(currentframe, cv2.COLOR_BGR2RGB)
        frameRgb = cv2.transpose(frameRgb)
        frameSurface = pygame.surfarray.make_surface(frameRgb)
        
        window.blit(frameSurface, (0, 0))
        pygame.display.update()


        #QRコードの検出
        if currentTime - lastScanedTime >= intervalTime:
            qrData = qrScanner(currentframe)
            if qrData:
                print(qrData)
                lastScanedTime = currentTime

        
        clock.tick(30)
        #メインループ終了

        
    cam.release()
    pygame.quit()
    
if __name__ == "__main__":
    main()

