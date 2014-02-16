//#include <EEPROM.h>
#include "Game.h"
#include "Utils.h"
Snake* snake;
char input;

void setup() {
  Serial.begin(500000);
  Serial.println("Game Start!");
  snake = new Snake();
}
void loop() {
  Utils::ClearScreen();
  switch(input){
    case 'A': // up
      Serial.println("UP!");
      break;
    case 'B': //down
      Serial.println("DOWN!");
      break;
    case 'C': // right
      Serial.println("RIGHT!");
      break;
    case 'D': // left
      Serial.println("LEFT!");
      break;
    default:
      snake->walk();
      break;
  }
  snake->print();
  delay(500);
}

void serialEvent() {
  char c;
  while((c = Serial.read()) != -1){
    input = c;
  }
  
//  snake->walk();
//  snake->debug();
//  Utils::PrintUptime();
}

