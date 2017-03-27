int sensorValue = 0;  //value read from the pot

void setup() {
  //init serial communications at 9600 bps;
  Serial.begin(9600);

}
void loop(){
  if (Serial.available()>0)
  {
    char inByte = Serial.read();
    switch(inByte)
    {
      case 'r': //Data request
        //read A0
        int sensorValue = analogRead(A0);
        float voltage = sensorValue * (5.0 / 1023.0);
        // print out the value you read:
        Serial.println(voltage, 8);
        break;
      }
    }
}
