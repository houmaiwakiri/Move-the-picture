import cv2

# 顔検出のためのカスケード分類器を読み込む
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# カメラを開く。外部カメラは1
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(2)

while True:
  # フレームを読み込む
  ret, frame = cap.read()
    
  ret, frame = cap.read()
  if not ret:
    print("カメラからのフレーム取得に失敗しました。")
    break

  # グレースケールに変換
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

  # 顔を検出
  faces = face_cascade.detectMultiScale(gray, 1.3, 5)

  # 検出された顔に四角形を描く
  for (x, y, w, h) in faces:
    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

  # フレームを表示
  cv2.imshow('Webcam', frame)

  # 'q'キーを押すと終了
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# カメラとウィンドウを解放
cap.release()
cv2.destroyAllWindows()
