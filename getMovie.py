import cv2

# カメラを開く
cap = cv2.VideoCapture(0)

while True:
    # フレームを読み込む
    ret, frame = cap.read()

    # 映像が正常に取得できたら表示
    if ret:
        cv2.imshow('Webcam', frame)

    # 'q'キーを押すと終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# カメラとウィンドウを解放
cap.release()
cv2.destroyAllWindows()
