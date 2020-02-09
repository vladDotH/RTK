#include <Servo.h>

enum Mode {
  DIGITAL = 2,
  PWM,
  
  SERVO
};

int servo_pins[7] = {15, 2, 4, 16, 17, 5, 18};
Servo servos[7];

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 7; i++) {
    servos[i].attach(servo_pins[i]);
  }
}

byte msg [3];
int byteCount = 0;

void loop() {
  if (Serial.available()) {
    msg[byteCount] = Serial.read();
    byteCount ++;
  }

  if (byteCount == 3) {
    if ( msg[0] == DIGITAL ) {
      digitalWrite( msg[1], msg[2] );
    }
    
    if (msg[0] == SERVO && msg[1] < 7 && msg[1] >= 0) {
      int pos = msg[2];
      
      if (pos > 177)
        pos = 177;
      if (pos < 3)
        pos = 3;
        
      servos[msg[1]].write(pos);
    }

    byteCount = 0;
  }
}
