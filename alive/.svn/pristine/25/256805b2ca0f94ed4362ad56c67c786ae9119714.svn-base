#ifndef _GAME_H
#define _GAME_H
#include "QueueArray.h"

enum Direction{
  Left,
  Up,
  Right,
  Down,
};
const int WIDTH = 50;
const int HEIGHT = 12;

struct Position{
public:
  int x;
  int y;
  Position(const int& x, const int& y){
    this->x = x;
    this->y = y;
  }
  Position(const Position& source){
    // Serial.println("||Copy Construct Called.||");
    this->x = source.x;
    this->y = source.y;
  }
  void Print(String prefix){
    Serial.println(prefix + String(" position: x, y = ") + x + ", "+ y);
  }
};

class Snake{
public:
  static const int START_X = 4;
  static const int START_Y = 4;
  Snake(){
    snakeBody.setPrinter(Serial);
    snakeBody.push(Position(START_X, START_Y));
    snakeBody.push(Position(START_X + 1, START_Y));
    snakeBody.push(Position(START_X + 2, START_Y));
    Serial.print(String("snakeBody.count() is ") + snakeBody.count());
    direction = Right;
  }
private:
  QueueArray<Position> snakeBody;
  Direction direction;
public:
  void walk(){
    Position tail = snakeBody.pop();
    // Serial.println(String("snakeBody.count() is ") + snakeBody.count());
    // tail.Print(String("tail"));

    Position head = snakeBody[snakeBody.count() - 1];
    // Serial.println("snake head");
    Position newHead(head.x + 1, head.y);
    snakeBody.push(newHead);
  }
  void debug(){
    //snakeBody.Debug();
    int length = snakeBody.count();
    for (int i = 0; i < length; i++){
      Position pos = snakeBody[i];
      pos.Print(String("snake body ") + i + String(": ") + pos.x + ", " + pos.y);
    }
  }
  void print(){
    char screen[HEIGHT + 1][WIDTH + 1];
    memset(screen, '.', sizeof(screen));
    
    for (int i = 0; i < snakeBody.count(); i++){
      Position body = snakeBody[i];
      screen[body.y][body.x] = '*';
    }
    String result;
    const String CRLF = String("\r\n");
    for (int i = 0; i < HEIGHT; i++){
      screen[i][WIDTH] = '\0'; // set string end mark
      result += screen[i] + CRLF;
    }
    Serial.println(result);
  }
};
#endif // _GAME_H
