import cv2
import easyocr
import numpy as np

# Load OCR 1 lần duy nhất (tránh crash Flask)
reader = easyocr.Reader(['en'], gpu=False)

# ==============================
# HÀM DETECT BIỂN SỐ
# ==============================
def detect_plate(frame):

    # resize ảnh để xử lý nhanh + dễ detect
    frame = cv2.resize(frame, (800, 600))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # tăng contrast cực mạnh (rất quan trọng)
    gray = cv2.equalizeHist(gray)

    # lọc nhiễu
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # nhị phân hoá thích nghi (cứu biển trong mọi ánh sáng)
    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        19, 9
    )

    # giãn nở để nối ký tự biển
    kernel = np.ones((5,5), np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=1)

    # tìm contour
    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    print("Tìm thấy", len(contours), "contours")

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        area = w * h
        ratio = w / float(h)

        # 🔥 THÔNG SỐ BIỂN SỐ VIỆT NAM
        if area > 4000 and 2 < ratio < 6:
            plate = frame[y:y+h, x:x+w]
            print("✅ Đã detect biển")
            return plate

    print("❌ Không detect được biển")
    return None


# ==============================
# HÀM OCR ĐỌC BIỂN SỐ
# ==============================
def read_text_from_plate(plate_img):
    if plate_img is None:
        return None

    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)

    # tăng độ tương phản
    gray = cv2.resize(gray, None, fx=2, fy=2,
                      interpolation=cv2.INTER_CUBIC)

    _, thresh = cv2.threshold(gray, 120, 255,
                              cv2.THRESH_BINARY)

    result = reader.readtext(thresh)

    if len(result) == 0:
        print("❌ OCR fail")
        return None

    plate_text = result[0][1]
    plate_text = plate_text.replace(" ", "").upper()

    print("✅ OCR:", plate_text)
    return plate_text


# ==============================
# 
# ==============================

def read_plate(plate_img):
    try:
        print("🔎 Đang đọc ký tự trên biển...")
        
        # chuyển ảnh sang xám
        gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)

        # tăng tương phản để OCR dễ đọc
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

        # OCR
        results = reader.readtext(thresh)

        text = ""
        for (bbox, txt, prob) in results:
            text += txt + " "

        text = text.strip()
        print("📄 Biển số đọc được:", text)

        if text == "":
            return None
        
        return text

    except Exception as e:
        print("❌ OCR lỗi:", e)
        return None




# ==============================
# HÀM MỞ CAMERA CHỤP BIỂN SỐ
# ==============================
def get_plate_from_camera():

    print("📸 Camera đang khởi động...")

    # ⚠️ webcam rời thường là index 1
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("❌ Không mở được camera")
        return None

    print("Nhấn SPACE để chụp ảnh - Nhấn ESC để thoát")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Không đọc được frame")
            break

        # hiển thị camera
        cv2.imshow("CAMERA", frame)

        # ⚠️ QUAN TRỌNG: phải có waitKey mới bắt được phím
        key = cv2.waitKey(1) & 0xFF

        # nhấn ESC để thoát
        if key == 27:
            print("Thoát camera")
            cap.release()
            cv2.destroyAllWindows()
            return None

        # nhấn SPACE để chụp
        if key == 32:
            print("📸 Đang chụp ảnh...")
            break

    cap.release()
    cv2.destroyAllWindows()

    # detect + OCR
    plate_img = detect_plate(frame)

    if plate_img is None:
        return None

    text = read_plate(plate_img)
    return text