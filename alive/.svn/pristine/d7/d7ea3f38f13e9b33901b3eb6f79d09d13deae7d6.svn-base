#ifndef _UTILS_H
#define _UTILS_H
class Utils{
public:
  static void ClearScreen(){
    Serial.write(27);       // ESC command
    Serial.print("[2J");    // clear screen command
    Serial.write(27);
    Serial.print("[H");     // cursor to home command
  }
  static void PrintUptime(){
    Serial.println(String("Program has started ") + millis()/100 + String(" seconds."));
  }
};
#endif // _UTILS_H
