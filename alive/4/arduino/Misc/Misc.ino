void setup(){
  int* a = new int();
  delete a;
  int * b = (int*)malloc(sizeof(int));
  free(b);
  
  Serial.begin(9600);
  int i=0;
  while(true){
    i++;
    if (!(i%10000)){
      Serial.print(millis()/100);
      Serial.print("s, i=");
      Serial.println(i);
    }
  }
}

void loop(){
}

