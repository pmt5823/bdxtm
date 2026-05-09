import serial
import time

#  sửa COM cho đúng máy bạn
SERIAL_PORT = "COM3"
BAUD_RATE = 9600

def open_barrier():
    try:
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # đợi Arduino reset

        arduino.write(b'O')   # gửi lệnh OPEN
        print(" Đã mở barie")

        arduino.close()

    except:
        print(" Không kết nối được Arduino")