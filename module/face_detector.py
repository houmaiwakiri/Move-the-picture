import cv2
import pygame
import os
from deepface import DeepFace

def load_image(image_path):
    return pygame.image.load(image_path)

def start_face_detection():
    # 顔検出のためのカスケード分類器を読み込む
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Pygameを初期化
    pygame.init()

    # ウィンドウサイズ設定
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Move Image with Webcam")

    # 画像を読み込む
    base_dir = os.path.dirname(os.path.abspath(__file__))  # 現在のファイルの絶対パス
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

    while True:
        # Pygameのイベント処理
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

        # 表情認識をDeepFaceで行う
        try:
            # DeepFaceで表情認識を行う
            analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            # 最も強い感情を取得
            emotion = analysis[0]['dominant_emotion']
        except Exception as e:
            print("Error in emotion analysis:", e)
            emotion = "neutral"  # エラー時はデフォルトでneutral

        # 画像を更新
        image = images.get(emotion, images["neutral"])
        image_rect = image.get_rect()

        # 顔が検出されたら、その位置に画像を移動
        for (x, y, w, h) in faces:
            image_rect.center = (x + w // 2, y + h // 2)

        # ウィンドウを塗りつぶす
        screen.fill((0, 0, 0))

        # 画像を描画
        screen.blit(image, image_rect)

        # 画面を更新
        pygame.display.flip()

        # 'q'キーで終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # カメラとウィンドウを解放
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    start_face_detection()
