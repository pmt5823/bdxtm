import cv2
import pytesseract
import numpy as np

# đường dẫn tesseract (bắt buộc)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def read_plate():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 👉 resize cho dễ xử lý
        frame = cv2.resize(frame, (640,480))

        # ===== XỬ LÝ ẢNH TRƯỚC OCR =====
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # giảm nhiễu
        blur = cv2.bilateralFilter(gray, 11, 17, 17)

        # tăng tương phản
        thresh = cv2.adaptiveThreshold(
            blur,255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,11,2)

        # tìm cạnh
        edges = cv2.Canny(thresh, 30, 200)

        # tìm contour
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        plate_img = None

        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.018 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4:   # hình chữ nhật -> khả năng là biển số
                x,y,w,h = cv2.boundingRect(cnt)
                plate_img = frame[y:y+h, x:x+w]
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                break

        plate_text = ""

        if plate_img is not None:
            gray_plate = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
            _, plate_thresh = cv2.threshold(gray_plate, 120,255,cv2.THRESH_BINARY)

            # OCR chỉ đọc chữ + số
            config = "--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-"
            plate_text = pytesseract.image_to_string(plate_thresh, config=config)

            cv2.imshow("Plate", plate_thresh)

        # hiển thị text lên camera
        cv2.putText(frame, plate_text, (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0,255,0),2)

        cv2.imshow("Camera", frame)

        # nhấn Q để chụp
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    return plate_text.strip()