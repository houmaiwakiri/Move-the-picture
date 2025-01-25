import cv2
import pygame
import os
from deepface import DeepFace

def load_image(image_path):
    return pygame.image.load(image_path)

def start_face_detection():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("喜怒哀楽")

    # 画像を読み込む
    base_dir = os.path.dirname(os.path.abspath(__file__))
    images = {
        "happy": load_image(os.path.join(base_dir, 'img', 'happy.png')),
        "sad": load_image(os.path.join(base_dir, 'img', 'sad.png')),
        "angry": load_image(os.path.join(base_dir, 'img', 'angry.png')),
        "surprised": load_image(os.path.join(base_dir, 'img', 'surprised.png')),
        "neutral": load_image(os.path.join(base_dir, 'img', 'neutral.png'))
    }
    image_rect = images["neutral"].get_rect()

    # カメラを開く
    cap = cv2.VideoCapture(0)

    # 常に読み込み続けるために無限ループ
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                exit()

        # カメラ映像を取得
        ret, frame = cap.read()

        # OpenCVで顔を検出
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # 表情認識
        try:
            #感情を取得し、認識できない場合エラー
            analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=True)
            emotion = analysis[0]['dominant_emotion']
        except Exception:
            # エラー時は真顔
            emotion = "neutral"

        # 画像更新
        image = images.get(emotion, images["neutral"])
        image_rect = image.get_rect()

        # 顔検出位置に画像を移動
        for (x, y, w, h) in faces:
            image_rect.center = (x + w // 2, y + h // 2)

        #背景を黒に
        screen.fill((0, 0, 0))

        # 画像表示
        screen.blit(image, image_rect)

        # 画面更新
        pygame.display.flip()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # カメラとウィンドウを解放
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    start_face_detection()
