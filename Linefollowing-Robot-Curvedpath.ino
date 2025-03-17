#include <Servo.h>                           // Include servo library
 
Servo servoRight;                            // Declare right servo
Servo servoLeft;                            // Declare left servo

// These constants won't change. They're used to give names to the pins used:
const int analogInPinLeft = A2;  // Analog input pin that the potentiometer is attached to
const int analogInPinRight = A0;  // Analog input pin that the potentiometer is attached to
//const int analogOutPin = 9;  // Analog output pin that the LED is attached to

int sensorValueLeft = 0;        // value read from the pot
int sensorValueRight = 0;        // value read from the pot

const int thresholdLeft = 100;  // Adjust this threshold to differentiate between black and white for the left sensor
const int thresholdRight = 120; // Adjust this threshold to differentiate between black and white for the right sensor
 
void setup()                                 // Built in initialization block
{
  servoRight.attach(10); // Attach the right servo to pin 10
  servoLeft.attach(11); // Attach the left servo to pin 11

  Serial.begin(9600);
}  
 
void loop()                                  // Main loop auto-repeats
{     
  // read the analog in value:
  sensorValueLeft = analogRead(analogInPinLeft);
  sensorValueRight = analogRead(analogInPinRight);

  // Determine the sensor states
  bool isLeftBlack = (sensorValueLeft < thresholdLeft);
  bool isRightBlack = (sensorValueRight < thresholdRight);
  
  // print the results to the Serial Monitor:
  Serial.print("sensorleft = ");
  Serial.print(sensorValueLeft);
  Serial.print("\nsensorRight = ");
  Serial.print(sensorValueRight);

  // Line-following logic
  
  if (!isLeftBlack && !isRightBlack) {
    servoLeft.writeMicroseconds(1700); // Left wheel Forward
    servoRight.writeMicroseconds(1300); // Right wheel  Forward
  }
  else if (isLeftBlack && !isRightBlack) {
      
    servoLeft.writeMicroseconds(1500); // Left wheel Turning Left
    servoRight.writeMicroseconds(1300); // Right wheel Turning Left

    
  }
  else if (!isLeftBlack && isRightBlack) {

     servoLeft.writeMicroseconds(1600); // Left wheel Turning Right
    servoRight.writeMicroseconds(1500); // Right wheel Turning Right
      

  }
  else {
    //Stop
    servoLeft.writeMicroseconds(1500); // Left wheel IDLE
    servoRight.writeMicroseconds(1500); // Right wheel  IDLE
  }  

  // wait 2 milliseconds before the next loop for the analog-to-digital
  // converter to settle after the last reading:
delay(2);
}