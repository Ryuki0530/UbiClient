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


session = requests.Session()

#カメラの宣言と初期化
def initializeCamera():
    print("Initializing camera...")
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

#通信処理
def makeRequest(url,data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        response = session.post(url, headers=headers, data=data)  # クッキーが自動で送信される
        print("HTTPレスポンスコード",response.status_code)
        print("レスポンス内容 :",response.text)
        return response.text
    except Exception as Err:
        print(f"リクエストエラー :{Err}")
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
        
        window.blit(frameSurface, (50, 50))
        pygame.display.update()


        #QRコードの検出
        if currentTime - lastScanedTime >= intervalTime:
            qrData = qrScanner(currentframe)
            if qrData:
                makeRequest(BACKEND_API,qrData)
                #print(qrData)
                lastScanedTime = currentTime


        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        
        clock.tick(30)
        #メインループ終了

        
    cam.release()
    pygame.quit()
    
if __name__ == "__main__":
    main()

