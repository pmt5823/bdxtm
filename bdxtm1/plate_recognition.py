import cv2
import pytesseract
import numpy as np

# đường dẫn Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# ================= DETECT BIỂN SỐ =================
def detect_plate(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # tăng tương phản mạnh
    gray = cv2.equalizeHist(gray)

    # làm mượt nhưng vẫn giữ cạnh
    blur = cv2.bilateralFilter(gray, 11, 17, 17)

    # phát hiện cạnh
    edged = cv2.Canny(blur, 30, 200)

    # giãn cạnh để nối các ký tự
    kernel = np.ones((5,5), np.uint8)
    edged = cv2.dilate(edged, kernel, iterations=1)

    contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # sắp xếp theo diện tích
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        ratio = w / h
        area = w * h

        # điều kiện mới chuẩn biển VN
        if 2 < ratio < 6 and 2000 < area < 50000:

            plate = frame[y:y+h, x:x+w]

            print("🎯 FOUND PLATE REGION")

            cv2.imshow("Detected Plate", plate)
            cv2.waitKey(500)

            return plate

    return None


# ================= OCR BIỂN SỐ =================
def read_plate(plate_img):

    try:
        plate = cv2.resize(plate_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)

        _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
        thresh = 255 - thresh

        cv2.imshow("OCR Image", thresh)
        cv2.waitKey(1)

        config = "--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789."

        text = pytesseract.image_to_string(thresh, lang="eng", config=config)

        text = text.strip().replace("\n","").replace(" ","")

        if len(text) < 6:
            print("❌ OCR fail")
            return None

        return text

    except:
        print("❌ OCR lỗi")
        return None


# ================= MỞ CAMERA & NHẬN DIỆN =================
def get_plate_from_camera():
    cap = cv2.VideoCapture(1)   # webcam rời

    if not cap.isOpened():
        print("❌ Không mở được camera")
        return None

    print("📸 Camera đang khởi động...")
    
    # cho camera warm up 2 giây
    for i in range(30):
        ret, frame = cap.read()

    print("📸 Đang chụp ảnh...")

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("❌ Không chụp được ảnh")
        return None

    cv2.imshow("Captured", frame)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()

    # ===== Detect biển =====
    plate_img = detect_plate(frame)

    if plate_img is None:
        print("❌ Không detect được biển")
        return None

    print("✅ Đã detect biển")

    # ===== OCR =====
    plate = ocr_plate(plate_img)

    if plate == "":
        print("❌ OCR fail")
        return None

    print("✅ Biển số:", plate)
    return plate