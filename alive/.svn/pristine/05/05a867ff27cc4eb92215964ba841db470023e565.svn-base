#include <EEPROM.h>

void setup() {
  // initialize serial:
  Serial.begin(9600);
  Serial.print("Enter to start: ");
}

void clearEEPROM(){
  // write a 0 to all 512 bytes of the EEPROM
  for (int i = 0; i < 512; i++)
    EEPROM.write(i, 0);
  // turn the LED on when we're done
}
void loop() {
}

void serialEvent() {
//  while (Serial.available()) {
//    // get the new byte:
//    char inChar = (char)Serial.read();
//    Serial.print(inChar);
//    Serial.print(' ');
//  }
  char inChar = (char)Serial.read();
  if (inChar == '\n' || inChar == 'y'){
    clearEEPROM();
    Serial.println("done!");
  }
  else{
    Serial.println(int(inChar));
  }
}

