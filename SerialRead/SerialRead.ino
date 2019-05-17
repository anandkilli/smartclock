
#include <SoftSerial.h>
#include <TinyPinChange.h>

SoftSerial mySerial(2, 3); // RX, TX
// ATTINY 2 => RPI GPIO 14
// ATTINY 3 => RPI GPIO 15
int Red = 0;
int Green = 1;
int Blue = 4;

//Some initial values for RGB
String RValue = "200";
String GValue = "50";
String BValue = "200";

void setup()  
{
  //Set pin mode to OUTPUT
  pinMode(Red, OUTPUT);
  pinMode(Green, OUTPUT);
  pinMode(Blue, OUTPUT);
  // set the data rate for the SoftwareSerial port
  mySerial.begin(9600);
  
}

void loop() // run over and over
{
    if (mySerial.available()) {
      String op = "";
      while(mySerial.available())
      op = op.concat((char)mySerial.read());

      //RPI send color in the format string "R:50 G:150 B:85"
      RValue = op.substring(op.indexOf("R")+2,op.indexOf(" "));
      GValue =  op.substring(op.indexOf("G")+2,op.indexOf(" ",op.indexOf("G")));
      BValue =  op.substring(op.indexOf("B")+2);
      //Let RPI know that the color is received
      mySerial.print("Updated");
      mySerial.println();
    }
    analogWrite(Red,RValue.toInt());
    analogWrite(Green,GValue.toInt());
    analogWrite(Blue,BValue.toInt());
    delay(100);
}
