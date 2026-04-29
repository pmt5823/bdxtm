import cv2

cap = cv2.VideoCapture(0)  # 0 = camera laptop

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # nhấn ESC để thoát
        break

cap.release()
cv2.destroyAllWindows()