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
int getRangeAdjustedValues(int value, int details[3])
{
  int leftBound = details[1];
  int rightBound = details[2];
  int diff = leftBound - rightBound;
  float retval = float(leftBound) - ((float(value)/100)*float(diff));
  return int(retval);
}
#include <Servo.h>
Servo CT;
Servo GT;
Servo RL;
Servo CL;
Servo GL;

float values[5];
Servo servos[5];
int details[5][3] = {{5, 140, 30},{6, 170, 10},{9, 120, 60},{10,120,60},{11,120,60}};
int fake_numbers[5][100];
int counter=0;

void setup() {
  Serial.begin(9600);
  while(!Serial);
  for(int i=0; i<5; i++)
  {
    fake_numbers[i][0] = 50;
    for(int j=1; j<100; j++)
    {
      fake_numbers[i][j] = fake_numbers[i][j-1] + random(-1,2);
      if(fake_numbers[i][j] < 20)
      {
        fake_numbers[i][j] = 20;
      }
      if(fake_numbers[i][j] > 90)
      {
        fake_numbers[i][j] = 90;
      }
    }
  }

  CT.attach(5);
  GT.attach(6);
  RL.attach(9);
  CL.attach(10);
  GL.attach(11);


  servos[0]=CT;
  servos[1]=GT;
  servos[2]=RL;
  servos[3]=CL;
  servos[4]=GL;

  for(int percentage =0; percentage<=100; percentage=percentage+1)
  {
    for(int i = 0; i < 5; i++)
    {
      Servo tmp_servo = servos[i];
      int servoAngle = getRangeAdjustedValues(percentage, details[i]);
      tmp_servo.write(servoAngle);
    }
    delay(25);
  }
  for(int percentage =100; percentage>=0; percentage=percentage-1)
  {
    for(int i = 0; i < 5; i++)
    {
      Servo tmp_servo = servos[i];
      int servoAngle = getRangeAdjustedValues(percentage, details[i]);
      tmp_servo.write(servoAngle);
    }
    delay(25);
  }
}

void loop()
{
  for(int i=0; i<5;i++)
  {
    Servo tmp_servo = servos[i];
    int servoAngle = getRangeAdjustedValues(fake_numbers[i][counter], details[i]);
    tmp_servo.write(servoAngle);
  }
  delay(1000);
  counter++;
  if (counter>99)
  {
    counter=0;
  }
}