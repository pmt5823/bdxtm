import cv2
import pytesseract
from parking_system import car_enter, car_exit

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape

    # Khung đặt biển số
    x1, y1 = int(w*0.3), int(h*0.4)
    x2, y2 = int(w*0.7), int(h*0.6)

    cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
    cv2.putText(frame,"Dat bien so vao khung",(x1,y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

    roi = frame[y1:y2, x1:x2]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)

    text = pytesseract.image_to_string(thresh, config='--psm 8')
    plate = text.strip().replace(" ", "").replace("\n","")

if len(plate) >= 6:   # lọc chữ rác
    print("Biển số đọc được:", plate)

    key = input("Nhấn i = vào | o = ra : ")

    if key == "i":
        car_enter(plate)
    elif key == "o":
        car_exit(plate)

    text = text.strip()

    if text != "":
        cv2.putText(frame,text,(x1,y2+40),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    cv2.imshow("Parking Camera", frame)

    key = cv2.waitKey(1)
    if key == 32:  # nhấn SPACE
        print("Bien so:", text)
        with open("plates.txt","a") as f:
            f.write(text+"\n")

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()