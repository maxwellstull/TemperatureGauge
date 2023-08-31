int getRangeAdjustedValues(int value, int details[3]) {
  int leftBound = details[1];
  int rightBound = details[2];
  int diff = leftBound - rightBound;
  float retval = float(leftBound) - ((float(value) / 100) * float(diff));
  return int(retval);
}
#include <Servo.h>
Servo CT;
Servo GT;
Servo RL;
Servo CL;
Servo GL;

String input_string = "";
int values[5];
int last_values[5];
Servo servos[5];
int details[5][3] = { { 5, 140, 30 }, { 6, 170, 10 }, { 9, 120, 60 }, { 10, 120, 60 }, { 11, 120, 60 } };


void setup() {
  Serial.begin(9600);
  input_string.reserve(200);
  while (!Serial)
    ;

  CT.attach(5);
  GT.attach(6);
  RL.attach(9);
  CL.attach(10);
  GL.attach(11);


  servos[0] = CT;
  servos[1] = GT;
  servos[2] = RL;
  servos[3] = CL;
  servos[4] = GL;

  for (int percentage = 0; percentage <= 100; percentage = percentage + 1) {
    for (int i = 0; i < 5; i++) {
      Servo tmp_servo = servos[i];
      int servoAngle = getRangeAdjustedValues(percentage, details[i]);
      tmp_servo.write(servoAngle);
    }
    delay(25);
  }
  for (int percentage = 100; percentage >= 0; percentage = percentage - 1) {
    for (int i = 0; i < 5; i++) {
      Servo tmp_servo = servos[i];
      int servoAngle = getRangeAdjustedValues(percentage, details[i]);
      tmp_servo.write(servoAngle);
    }
    delay(25);
  }
}

void loop() {
  while (Serial.available() == 0) {}
  readSerial();
  for(int i=0; i<5; i++)
  {
    if (abs(values[i] - last_values[i]) > 2){
    Servo tmp_servo = servos[i];
    tmp_servo.attach(details[i][0]);}
  }
  delay(100);
  for (int i = 0; i < 5; i++) {
    Servo tmp_servo = servos[i];
    if (abs(values[i] - last_values[i]) > 2) {
      int servoAngle = getRangeAdjustedValues(values[i], details[i]);
      tmp_servo.write(servoAngle);
      last_values[i] = values[i];
    }
  }
  delay(100);
    for(int i=0; i<5; i++)
  {
    Servo tmp_servo = servos[i];
    tmp_servo.detach();
  }
}
void readSerial() {
  if (Serial.available() > 0) {
    input_string = Serial.readStringUntil('\n');
  }

  values[0] = input_string.substring(0, 3).toInt();
  values[1] = input_string.substring(3, 6).toInt();
  values[2] = input_string.substring(6, 9).toInt();
  values[3] = input_string.substring(9, 12).toInt();
  values[4] = input_string.substring(12, 15).toInt();

  Serial.write('1');
}