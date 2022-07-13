#include "Ultrasonic.h"
#include <a7gprsnew.h>


a7gprsnew device;

const int echoPin = 5; //PINO DIGITAL UTILIZADO PELO HC-SR04 ECHO(RECEBE)
const int trigPin = 4; //PINO DIGITAL UTILIZADO PELO HC-SR04 TRIG(ENVIA)
Ultrasonic ultrasonic(trigPin,echoPin); 
String a = "1";
double val = 0;
int porcentagem = 0;
int horas,minuntos,segundos;
String dia,mes,ano;
int dia_int,mes_int,ano_int;
int media=0;
float porDist = 0; 
String data ;
String bateria;
void setup() {
  
  Serial.begin(115200);
  Serial.println("Start");  
  pinMode();
  pinMode(echoPin, INPUT); //DEFINE O PINO COMO ENTRADA (RECEBE)
  pinMode(trigPin, OUTPUT); //DEFINE O PINO COMO SAIDA (ENVIA)
  
}

void loop() {
  bool r;
  //for(int j = 0;j < 10;j++){ 
    Serial.print("Distancia: "); //IMPRIME O TEXTO NO MONITOR SERIAL
    for(int i = 0;i < 21; i++){
      media = media + hcsr04();
    }
  
    media = media/20;
    delay(1000);
    Serial.print(media); 
    Serial.println(" cm"); 
    porDist = (media/160.0)*100;
    Serial.print(porDist); 
    Serial.println(" %"); 
  
    //if((porDist >= 20 && porDist <= 30 ) || (porDist >= 40 && porDist <= 50 ) || (porDist >= 75 && porDist <= 101) ){
      device.init();  
      bateria = device.get_baterry();
      if(bateria.toInt() == 10){
        bateria = "100";
        }
      String data = String(media)+","+bateria+","+converte_time(device.get_time());
      if(horas >= 0 && horas <=5){
        device.Sleep();
        
        //esp_deep_sleep(18000000000);
        }
      if(bateria.toInt() > 11 && bateria.toInt() <= 30 ){
        device.Sleep();
        
        //esp_deep_sleep(10800000000);
        }
        
      do{
        r = device.send_data(String(data), "cm,%,day,hours","distTrashGreen,battery,time");
          if(!r) {
            device.reboot();
          }
      }while(!r);
       device.Sleep();
      // break; 
      
    //}
  //}
//esp_deep_sleep(10800000000);
Serial.println("De novo");
  
}


//-------------------------------------------------------------------------------------------------------------------


int hcsr04(){
    digitalWrite(trigPin, LOW); //SETA O PINO 6 COM UM PULSO BAIXO "LOW"
    delayMicroseconds(2); //INTERVALO DE 2 MICROSSEGUNDOS
    digitalWrite(trigPin, HIGH); //SETA O PINO 6 COM PULSO ALTO "HIGH"
    delayMicroseconds(10); //INTERVALO DE 10 MICROSSEGUNDOS
    digitalWrite(trigPin, LOW); //SETA O PINO 6 COM PULSO BAIXO "LOW" NOVAMENTE
    //FUNÇÃO RANGING, FAZ A CONVERSÃO DO TEMPO DE
    //RESPOSTA DO ECHO EM CENTIMETROS, E ARMAZENA
    //NA VARIAVEL "distancia"
    int distancia = (ultrasonic.Ranging(CM)); //VARIÁVEL GLOBAL RECEBE O VALOR DA DISTÂNCIA MEDIDA
    return distancia;
 }

String converte_time(String time){
  String aux1;
 // 21/04/20,0:11:20
  ano=time.substring(0,2); 
  mes=time.substring(3,5);
  dia=time.substring(6,8);
  horas = time.substring(9,11).toInt();
  ano_int=ano.toInt();
  mes_int=mes.toInt();
  dia_int=mes.toInt();
 
  
  if(horas == 0){
    horas = 24;
    dia = String(dia_int-1);
    if((mes_int == 4 || mes_int == 6 || mes_int == 9 || mes_int==11) && dia_int == 30 ){
       mes = String(mes_int-1);
      }
    if((mes_int == 1 || mes_int == 3 || mes_int == 5 || mes_int==8 || mes_int == 10 || mes_int==12)  && dia_int == 31){
        mes = String(mes_int-1);
      }
    if(mes_int == 2 && dia_int == 28 ){
      mes = String(mes_int-1);
      }
    if(mes_int == 12 && dia_int == 31){
        ano = String(ano_int-1);
      }
    
    }
  if(horas == 1){
    horas = 25;
    dia = String(dia_int-1);
    if((mes_int == 4 || mes_int == 6 || mes_int == 9 || mes_int==11) && dia_int == 30 ){
       mes = String(mes_int-1);
      }
    if((mes_int == 1 || mes_int == 3 || mes_int == 5 || mes_int==8 || mes_int == 10 || mes_int==12)  && dia_int == 31){
        mes = String(mes_int-1);
      }
    if(mes_int == 2 && dia_int == 28 ){
      mes = String(mes_int-1);
      }
    if(mes_int == 12 && dia_int == 31){
        ano = String(ano_int-1);
      }
  }
   if(horas == 2){
    dia = String(dia_int-1);
    horas = 26;
    if((mes_int == 4 || mes_int == 6 || mes_int == 9 || mes_int==11) && dia_int == 30 ){
       mes = String(mes_int-1);
      }
    if((mes_int == 1 || mes_int == 3 || mes_int == 5 || mes_int==8 || mes_int == 10 || mes_int==12)  && dia_int == 31){
        mes = String(mes_int-1);
      }
    if(mes_int == 2 && dia_int == 28 ){
      mes = String(mes_int-1);
      }
    if(mes_int == 12 && dia_int == 31){
        ano = String(ano_int-1);
    }
   }
  

  
   
  
  horas =  horas - 3;
  minuntos = time.substring(12,15);
  segundos = time.substring(15,17);
  
  Serial.println(dia);
  Serial.println(mes);
  Serial.println(ano);
  
    aux1=mes+"/"+dia+"/"+ano+","+ String(horas) + ":"+ String(minuntos)+":"+String(segundos);
 return aux1;
  
}
