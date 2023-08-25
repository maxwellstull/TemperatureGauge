/*int tempo;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  tempo = 3000;
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
  delay(tempo);                      // wait for a second
  digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
  delay(tempo);  
}

void serialEvent()
{
  while(Serial.available())
  {
    char ch = Serial.read();
    tempo = 500;
    Serial.write(ch);
  }
}*/
/*
int x;
void setup() {
 Serial.begin(115200);
 Serial.setTimeout(1);
}
void loop() {
 while (!Serial.available());
 x = Serial.readString().toInt();
 Serial.print(x + 1);
}
*/
#include <Servo.h>
Servo CT;
Servo GT;
Servo RL;
Servo CL;
Servo GL;
int angle = 0;
void setup() {
  CT.attach(6);
  GT.attach(9);
  RL.attach(10);
  CL.attach(11);
  GL.attach(13);
/*
  CT.write(90);
  GT.write(90);
  RL.write(90);
  CL.write(90);
  GL.write(90);
*/
  CT.write(135);
  GT.write(170);
  RL.write(120);
  CL.write(120);
  GL.write(120);
  delay(2000);

  CT.write(45);
  GT.write(10);
  RL.write(60);
  CL.write(60);
  GL.write(60);
  delay(2000);

  CT.write(135);
  GT.write(170);
  RL.write(120);
  CL.write(120);
  GL.write(120);
  delay(2000);

  GT.detach();
  
}

void loop()
{

}