import cv2
import easyocr
import numpy as np

# load OCR 1 lần duy nhất (rất quan trọng)
reader = easyocr.Reader(['en'])


# ================= CHUẨN HOÁ BIỂN SỐ =================
def normalize_plate(text):
    text = text.upper()

    replace_map = {
        "I": "1",
        "O": "0",
        "Z": "2",
        "S": "5",
        "B": "8",
        "_": "",
        " ": ""
    }

    for k, v in replace_map.items():
        text = text.replace(k, v)

    # regex biển VN: 2 số + chữ + 4-5 số
    match = re.findall(r'\d{2}[A-Z]\d{4,5}', text)

    if len(match) == 0:
        return None

    raw = match[0]

    # format lại đẹp: 30G12345 → 30G-123.45
    return f"{raw[:3]}-{raw[3:6]}.{raw[6:]}"


# ================= CHỤP ẢNH CAMERA =================
def capture_image():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Không mở được camera")
        return None

    print("Camera đang chạy...")
    print("Nhấn SPACE để chụp - ESC để thoát")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("CAMERA", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 32:  # SPACE
            print("Đã chụp ảnh")
            cap.release()
            cv2.destroyAllWindows()
            return frame

        elif key == 27:  # ESC
            cap.release()
            cv2.destroyAllWindows()
            return None


# ================= TÌM BIỂN SỐ =================
def detect_plate(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    print("Contours tìm thấy:", len(contours))

    for cnt in sorted(contours, key=cv2.contourArea, reverse=True)[:30]:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.018 * peri, True)

        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(cnt)

            ratio = w / h

            # lọc biển số VN
            if 1.2 < ratio < 6 and w > 100 and h > 30:
                plate = img[y:y+h, x:x+w]

                # vẽ khung xanh
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 3)
                cv2.imshow("DETECTED PLATE", img)
                cv2.waitKey(1000)
                cv2.destroyAllWindows()

                print("Đã phát hiện biển")
                return plate

    print("Không tìm thấy biển")
    return None


# ================= OCR ĐỌC BIỂN =================
def read_plate(plate_img):
    plate_img = cv2.resize(plate_img, None, fx=2, fy=2)

    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    kernel = np.ones((3,3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    cv2.imshow("OCR INPUT", thresh)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()

    results = reader.readtext(thresh, detail=0)

    if len(results) == 0:
        print("OCR không đọc được")
        return None

    text = "".join(results)
    text = text.replace(" ", "").upper()

    print("Biển đọc được:", text)
    return text


# ================= HÀM CHÍNH GỌI TỪ WEB =================
def get_plate_from_camera():
    frame = capture_image()
    if frame is None:
        return None

    plate = result[0]
    print("Biển AI đọc:", plate)

    plate = normalize_plate(plate)
    print("Biển sau chuẩn hoá:", plate)

    return plate

    plate_img = detect_plate(frame)
    if plate_img is None:
        return None

    plate_text = read_plate(plate_img)
    return plate_text