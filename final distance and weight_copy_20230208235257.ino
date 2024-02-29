#include <HX711_ADC.h>

#define max_distance 200
#include <HX711_ADC.h>

HX711_ADC LoadCell(4, 5); // dt pin, sck pin



const int HtrigPin = 6;
const int HechoPin = 7;

const int LtrigPin = 8;
const int LechoPin = 9;

const int WtrigPin = 10;
const int WechoPin = 11;

long durationH;
long durationL;
long durationW;

float weight;
float height;
float length;
float width; 
//int speakerPin = 12;
void setup() 
{  
  LoadCell.begin();
  LoadCell.start(1000);
  LoadCell.setCalFactor(20);

  pinMode(HtrigPin, OUTPUT);
  pinMode(HechoPin, INPUT);
  pinMode(LtrigPin, OUTPUT);
  pinMode(LechoPin, INPUT);
  pinMode(WtrigPin, OUTPUT);
  pinMode(WechoPin, INPUT);
  Serial.begin(115200);
  delay(500);
}

void loop() 
{ //////////////////////////////////Load Cell////////////////////////////////////////////
  LoadCell.update();
  weight = LoadCell.getData();


  ///////////////////////////////// Height///////////////////////////////////////////////
  // Write a pulse to the HC-SR04 Trigger Pin
  digitalWrite(HtrigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(HtrigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(HtrigPin, LOW);
  // Measure the response from the HC-SR04 Echo Pin
  durationH = pulseIn(HechoPin, HIGH);
  // Determine distance from duration
  // Use 343 metres per second as speed of sound
  height=113-(durationH*0.033/2); //111
  // Prints "Distance: <value>" on the first line of the LCD
  //////////////////////////////////Length/////////////////////////////////////////////////
  digitalWrite(LtrigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(LtrigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(LtrigPin, LOW);
  durationL = pulseIn(LechoPin, HIGH);
  length=92-(durationL*0.034/2); //122 92
  //////////////////////////////////Width/////////////////////////////////////////////////
  digitalWrite(WtrigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(WtrigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(WtrigPin, LOW);
  durationW = pulseIn(WechoPin, HIGH);
  width =93-(durationW*0.034/2); //122  93
Serial.print(width);
Serial.print(",");
Serial.print(length);
Serial.print(",");
Serial.print(height);
Serial.print(",");
Serial.println(weight);

delay(100);




}
