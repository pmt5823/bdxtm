import cv2

for i in range(5):
    print("Đang thử Camera", i)

    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)   # ⭐ QUAN TRỌNG

    if not cap.isOpened():
        print("❌ Cam", i, "không mở được")
        continue

    print("✅ Camera", i, "OK - bấm Q để chuyển cam")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Không đọc được frame")
            break

        cv2.imshow(f"Camera {i}", frame)

        # ⭐ KHÔNG dùng waitKey(0) nữa
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()