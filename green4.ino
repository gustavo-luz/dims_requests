#include "esp32SIM7600E.h"
#include <Wire.h>
#include <VL53L0X.h>

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif


VL53L0X sensor;
esp32SIM7600E device;

int bateria = 0 ;

bool envio = false;
bool r ; 


void setup() {
  Serial.begin(115200);
  Wire.begin();
  sensor.init();
  sensor.setTimeout(500);
  sensor.setSignalRateLimit(0.1);
  sensor.setVcselPulsePeriod(VL53L0X::VcselPeriodPreRange, 18);
  sensor.setVcselPulsePeriod(VL53L0X::VcselPeriodFinalRange, 14);
  pinMode(15,INPUT_PULLUP);
  digitalWrite(15,HIGH);
  sensor.startContinuous();
  
  if(!device.init()){
     device.Sleep(300);
    }

   
  
}

void loop() {
  
  float media=0;
  for(int i = 0;i < 10; i++){
      media = media + sensor.readRangeContinuousMillimeters();
    }
  Serial.print("Distance: ");
  Serial.print(media/100.0);
  Serial.println("cm");
  
  
  String data = String(media/100.0)+","+String(device.get_baterry())+","+device.getGPS();
  Serial.println(data);
  
  if(!device.connect()){
      device.Sleep(300);//time in seconds
    }

    
  do{
      r = device.send_data(data, "cm,%,Graus,Graus","distTrashGreen,battery,latitude,longitude");
      Serial.println(r);
        if(!r) {
           device.Sleep(300);//time in seconds
        }
    }while(!r);
    envio = true;

    device.Sleep(1200); //time in seconds
   
              
 }

 
