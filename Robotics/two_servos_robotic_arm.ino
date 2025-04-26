#include <Stepper.h>
#include <Servo.h>

// Define the number of steps per revolution (adjust to your motor spec)
const int stepsPerRevolution = 250;

// Initialize the stepper library with the motor interface pins
// IN1, IN2, IN3, IN4 (you can adjust these based on your wiring)
Stepper myStepper(stepsPerRevolution, 2, 4, 3, 5);

//servo wiring
//orange-->pin
//red -->5v
//brown-->ground
char sequence;
//char data;
Servo servo1;  // Shoulder
Servo servo2;  // Elbow
int num;

int dataPin = A0;   // SER (Pin 14 on 74HC595)
int clockPin = A1;  // SRCLK (Pin 11)
int latchPin = A2;  // RCLK (Pin 12)

byte digits[10] = {
  0b11000000, // 0 (a,b,c,d,e,f LOW)
  0b11111001, // 1 (b,c LOW)
  0b10100100, // 2 (a,b,g,e,d LOW)
  0b10110000, // 3 (a,b,g,c,d LOW)
  0b10011001, // 4 (f,g,b,c LOW)
  0b10010010, // 5 (a,f,g,c,d LOW)
  0b10000010, // 6 (a,f,g,e,c,d LOW)
  0b11111000, // 7 (a,b,c LOW)
  0b10000000, // 8 (all segments LOW)
  0b10010000  // 9 (a,b,c,d,f,g LOW)
};

const int trackingsensor_left = 8;
const int trackingsensor_right = 9;

// Motor control pins (L298N example)
const int motorLeft_A = 13;   // IN1 (Forward)
const int motorLeft_B = 12;   // IN2 (Backward)
const int motorRight_A = 11;  // IN3 (Forward)
const int motorRight_B = 10;  // IN4 (Backward)

// Speed settings
const int motorSpeed = 150;      // Base speed (0-255)
const int correctionSpeed = 200; // Correction speed (0-255)

unsigned long lastSeenTime = 0;
const unsigned long timeout = 300; // Timeout in milliseconds
void touch5(){
  //displayDigit(5);
    for (int pos = 40; pos <= 90; pos++) {
    servo1.write(pos+50);
    //if(pos<=90){
    servo2.write(pos);
    //}
    delay(35);
  }
  /*for (int pos = 40; pos <= 90; pos++) {
    servo2.write(pos);
    delay(15);
  }*/
  for (int pos = 150; pos >= 90; pos--) {
    servo1.write(pos);
    delay(15);
  }
 

  // Move elbow from 90 to 40 and back
  for (int pos = 90; pos >= 40; pos--) {
    servo2.write(pos);
    delay(15);
  }
  

  delay(1000); // Pause before restarting loop
  }
void touch2(){
  //displayDigit(2);
  for (int pos = 50; pos <= 120; pos++) {
    
    if(pos<=80){
    servo1.write(pos+30);
    }
    servo2.write(pos);
    delay(35);
  }
  for (int pos = 130; pos >=90; pos--) {
    servo1.write(pos);
    delay(15);
  }
  for (int pos =120; pos >= 40; pos--) {
    servo2.write(pos);
    delay(15);
  }
  delay(1000);
  }
void touch8(){
  //displayDigit(8);
  for (int pos = 40; pos <= 90; pos++) {
    servo1.write(pos+40);
    if (pos<=55){
    servo2.write(80-pos);
    }
    //if(pos<=80){
    //}
    delay(35);
  }
  for (int pos = 130; pos >=90; pos--) {
    servo1.write(pos);
    delay(15);
  }
  for (int pos =25; pos <= 40; pos++) {
    servo2.write(pos);
    delay(15);
  }
  delay(1000);
  }
  
void touch6(){
 // displayDigit(6);
  Serial.println("Turn Right");
  myStepper.step(stepsPerRevolution);
  delay(500);
  touch5();
  // Step backward
  Serial.println("Turn Left");
  myStepper.step(-stepsPerRevolution);
  delay(1000);
  }
void reboot(){
  //displayDigit(0);
    servo1.write(90);
    servo2.write(40);
  }
void touch4(){
 // displayDigit(4);
  Serial.println("Turn Left");
  myStepper.step(-stepsPerRevolution);
  touch5();
  Serial.println("Turn Right");
  myStepper.step(stepsPerRevolution);
  delay(500);
  
  // Step backward
  
  delay(1000);
  }  
void touch1(){
 // displayDigit(1);
  Serial.println("Turn Left");
  myStepper.step(-stepsPerRevolution);
  touch2();
  Serial.println("Turn Right");
  myStepper.step(stepsPerRevolution);
  delay(500);
  
  // Step backward
  
  delay(1000);
  }   
void touch7(){
  //displayDigit(7);
  Serial.println("Turn Left");
  myStepper.step(-stepsPerRevolution);
  touch8();
  Serial.println("Turn Right");
  myStepper.step(stepsPerRevolution);
  delay(500);
  
  // Step backward
  
  delay(1000);
  }    
void touch3(){
  
  //displayDigit(3);
  Serial.println("Turn Right");
  myStepper.step(stepsPerRevolution);
  touch2();
  Serial.println("Turn Left");
  myStepper.step(-stepsPerRevolution);
  delay(500);
  // Step backward
  
  delay(1000);
  }    
void touch9(){
 // displayDigit(9);
  
  Serial.println("Turn Right");
  myStepper.step(stepsPerRevolution);
  touch8();
  Serial.println("Turn Left");
  myStepper.step(-stepsPerRevolution);
  delay(500);
  // Step backward
  
  delay(1000);
  }      
void displayDigit(int num) {
  digitalWrite(latchPin, LOW);  // Prepare shift register
  shiftOut(dataPin, clockPin, MSBFIRST, digits[num]);  // Send data
  digitalWrite(latchPin, HIGH);  // Update output
  }  
void arrange(){
  char data = (char)(random(1, 10) + '0');
  Serial.println(data);
  int num=data-'0';
  displayDigit(num);
  delay(1000);
  
  //if (Serial.available()){
    //data=Serial.read();
  if (data=='5'){
      touch5();}
  else if (data=='2'){
      touch2();}
  else if(data=='8'){
      touch8();}
  else if(data=='6'){
      touch6();}  
  else if(data=='0'){
      reboot();}
  else if(data=='4'){
      touch4();}
  else if(data=='1'){
      touch1();} 
  else if(data=='3'){
      touch3();} 
  else if(data=='9'){
      touch9();} 
  else if(data=='7'){
      touch7();}   
  //turnLeft();
  //turnLeft();  
  turnRight();
  turnRight();
   /*
  analogWrite(motorLeft_A, 0);
  analogWrite(motorLeft_B, correctionSpeed);  // Left wheel reverses slightly
  analogWrite(motorRight_A, correctionSpeed * 4 );
  analogWrite(motorRight_B, 0);      
      */  
  //}
  /*
  // Move shoulder from 90 to 150 and back
  for (int pos = 40; pos <= 100; pos++) {
    servo1.write(pos+50);
    if(pos<=90){
    servo2.write(pos);}
    delay(15);
  }
  /*for (int pos = 40; pos <= 90; pos++) {
    servo2.write(pos);
    delay(15);
  }*//*
  for (int pos = 150; pos >= 90; pos--) {
    servo1.write(pos);
    delay(15);
  }

  // Move elbow from 90 to 40 and back
  for (int pos = 90; pos >= 40; pos--) {
    servo2.write(pos);
    delay(15);
  }
  

  delay(1000); // Pause before restarting loop
  */
  }
void moveForward() {
  analogWrite(motorLeft_A, motorSpeed);
  analogWrite(motorLeft_B, 0);
  analogWrite(motorRight_A, motorSpeed);
  analogWrite(motorRight_B, 0);
  }

void turnRight() {
  analogWrite(motorLeft_A, correctionSpeed);
  analogWrite(motorLeft_B, 0);
  analogWrite(motorRight_A, 0);
  analogWrite(motorRight_B, correctionSpeed/2); // Right wheel reverses slightly
  }

void turnLeft() {
  analogWrite(motorLeft_A, 0);
  analogWrite(motorLeft_B, correctionSpeed/2);  // Left wheel reverses slightly
  analogWrite(motorRight_A, correctionSpeed);
  analogWrite(motorRight_B, 0);
  }

void stopMotors() {
  analogWrite(motorLeft_A, 0);
  analogWrite(motorLeft_B, 0);
  analogWrite(motorRight_A, 0);
  analogWrite(motorRight_B, 0);
  }

void setup() {
  pinMode(trackingsensor_left, INPUT);
  pinMode(trackingsensor_right, INPUT);
  
  // Initialize motor pins
  pinMode(motorLeft_A, OUTPUT);
  pinMode(motorLeft_B, OUTPUT);
  pinMode(motorRight_A, OUTPUT);
  pinMode(motorRight_B, OUTPUT);
  
  // Start serial for debugging
  Serial.begin(115200);
  stopMotors(); // Ensure motors are off initially
  displayDigit(0);
  pinMode(dataPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(latchPin, OUTPUT);

  myStepper.setSpeed(60);
  servo1.attach(6);   // Attach shoulder servo to pin 6
  servo2.attach(7);  // Attach elbow servo to pin 7

  // Optional: Start in middle position
  servo1.write(90);
  servo2.write(40);
  delay(1000);
  //Serial.begin(9600);
  randomSeed(analogRead(0));
}

void loop() {
  int sensorvalue_left = digitalRead(trackingsensor_left);
  int sensorvalue_right = digitalRead(trackingsensor_right);
  
  // Debug output
  Serial.print("Left: ");
  Serial.print(sensorvalue_left);
  Serial.print(" | Right: ");
  Serial.println(sensorvalue_right);

  // Line-following logic
  /*
  if (sensorvalue_left == HIGH && sensorvalue_right == HIGH) {
    moveForward();
    Serial.println("ON TRACK - Moving forward");
  }
  else if (sensorvalue_left == LOW) {
    turnRight();
    Serial.println("OUT_OF_LINE: LEFT - Correcting right");
  }
  else if (sensorvalue_right == LOW) {
    turnLeft();
    Serial.println("OUT_OF_LINE: RIGHT - Correcting left");
  }
  else if (sensorvalue_left == LOW && sensorvalue_right == LOW) {
    Serial.println("Facing a WALL: Arrange");
    stopMotors();
    arrange();
    delay(500);
    turnLeft();
  }
  
  
  
  delay(50); // Small delay for stability
  */
  //the correct code is below this line
  
  if (sensorvalue_left == HIGH && sensorvalue_right == HIGH) {
    // Both sensors see the line - move forward
    moveForward();
    lastSeenTime = millis(); // Reset the timer
    Serial.println("ON TRACK - Moving forward");
  }
  else if (sensorvalue_left == LOW && sensorvalue_right == HIGH) {
    // Only right sensor sees the line - turn right
    turnRight();
    lastSeenTime = millis(); // Reset the timer
    Serial.println("OUT_OF_LINE: LEFT - Correcting right");
  }
  else if (sensorvalue_left == HIGH && sensorvalue_right == LOW) {
    // Only left sensor sees the line - turn left
    turnLeft();
    lastSeenTime = millis(); // Reset the timer
    Serial.println("OUT_OF_LINE: RIGHT - Correcting left");
  }
  else {
    // Both sensors don't see the line - check if we should stop
    if (millis() - lastSeenTime > timeout) {
      // We've been off the line for longer than the timeout - stop
      stopMotors();
      Serial.println("END OF LINE - Stopping");
      arrange();
      //delay(500);
      //turnLeft();
      
    }
    //else {
      // Just lost the line momentarily - continue last action briefly
      // (This helps with small gaps or imperfections in the line)
    //}
    delay(50);
}
}
