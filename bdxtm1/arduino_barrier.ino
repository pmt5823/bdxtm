#include <Servo.h>

Servo barrier;

int posClose = 10;   // góc đóng barie
int posOpen  = 90;   // góc mở barie

void setup() {
  Serial.begin(9600);
  barrier.attach(9);
  barrier.write(posClose); // đóng ban đầu
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "OPEN") {
      openBarrier();
    }
  }
}

void openBarrier() {
  barrier.write(posOpen);   // mở barie
  delay(5000);              // chờ xe đi qua
  barrier.write(posClose);  // đóng lại
}