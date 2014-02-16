#ifndef _QUEUEARRAYTEST_H
#define _QUEUEARRAYTEST_H

// include Arduino basic header.
#include <QueueArrayTest.h>
#include <Game.h>

class QueueArrayTest{
private:
  QueueArray<Position> intQueue;
  void TestPop(const Position& desired){
    Position result = intQueue.pop();
    if (result.x != desired.x || result.y != desired.y) PrintError(desired.x, result.x);
  }
  bool PrintError(int desiredValue, int actualValue){
    Serial.println(String("DesiredValue: ") + desiredValue + String("ActualValue: ") + actualValue);
  }
public:
  QueueArrayTest(){
  }
  void Run(){
    TestPushPop();
    TestIndex();
  }
  void TestPushPop(){
    Position p = Position(20, 20);
    Serial.println(String("*****:") + p.x);
    intQueue.push(p);
    intQueue.push(Position(10, 10));
    intQueue.push(Position(0, 0));
    TestPop(p);
    TestPop(Position(10, 10));
    TestPop(Position(0, 0));
    Serial.println("Push/Pop Test Done.");
  }
  void TestIndex(){
    intQueue.push(Position(20, 20));
    intQueue.push(Position(10, 10));
    intQueue.push(Position(0, 0));
    Position val = intQueue[0];
    if (val.x != 20) PrintError(20, val.x);
    val = intQueue[1];
    if (val.x != 10) PrintError(10, val.x);
    val = intQueue[2];
    if (val.x != 0) PrintError(0, val.x);
    Serial.println("IndexAt Test Done.");
  }
};
#endif // _QUEUEARRAYTEST_H
