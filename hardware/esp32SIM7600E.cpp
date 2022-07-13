#include "esp32SIM7600E.h"
#include "BluetoothSerial.h"


#define MODEM_TX            27
#define MODEM_RX            26
#define MODEM_PWRKEY        4
#define MODEM_DTR           32
#define MODEM_RI            33
#define MODEM_FLIGHT        25
#define MODEM_STATUS        34

#define LED_PIN             12

unsigned long start_time;
String buff = "0123456789012345678901234567890123456789012345678901234567890123456789";
unsigned long time0, time1;
BluetoothSerial SerialBT;

esp32SIM7600E::esp32SIM7600E(){}

bool esp32SIM7600E::init(){
	Serial1.begin(115200, SERIAL_8N1, MODEM_RX, MODEM_TX);
	SerialBT.begin("eletronica_e_programacao"); 
	Serial.println("start");
	SerialBT.println("BluetoothSerial rodando");
	start_time = millis();

	pinMode(LED_PIN, OUTPUT);
  	digitalWrite(LED_PIN, HIGH);
  	pinMode(MODEM_PWRKEY, OUTPUT);
  	digitalWrite(MODEM_PWRKEY, HIGH);
  	delay(400); //Need delay
  	digitalWrite(MODEM_PWRKEY, LOW);
  	pinMode(MODEM_FLIGHT, OUTPUT);
  	digitalWrite(MODEM_FLIGHT, HIGH);
	
	do{	
		int cout = 0;
		Serial1.println("AT");
		delay(100);
		this->read_esp32SIM7600E();
		if(buff.indexOf("ERROR") != -1){
			return false;
		}
		if(cout == 30){
			this->Sleep(300);
		}
		cout++;
	}while(buff.indexOf("OK") == -1 && check_uptime());
	
	return true;
}




bool esp32SIM7600E::check_uptime(){
	if(millis()-start_time > 420000){ 
		this->Sleep(300);
	}
	return true; 
}


void esp32SIM7600E::reboot(){

	digitalWrite(LED_PIN, LOW);
	delay(500);
	digitalWrite(MODEM_FLIGHT, LOW);
	delay(500);
	Serial1.println("AT+CPOF");
	delay(100);
	this->read_esp32SIM7600E();
	delay(120000);
	funcReset();

}

void esp32SIM7600E::read_esp32SIM7600E(){
	buff.remove(0,70); //Apagando buffer
	while (Serial1.available() && check_uptime()) {
		buff += Serial1.readString();
		Serial.println(buff); //For Debug Porpouses
		SerialBT.println(buff);
	}
}



bool esp32SIM7600E::connect(){
	long time = millis();
	buff.remove(0,70); //Apagando buffer
		
		
		
		
		//Serial1.println("AT+CSTT=""zap.vivo.com.br"",""vivo"",""vivo");
		//Serial1.println("AT+CSTT=""timbrasil.br"",""tim"",""tim");
		//Serial1.println("AT+CSTT=""claro.com.br"",""claro"",""claro");
		//Serial1.println("AT+CSTT=""gprs.oi.com.br"",""oi"",""oi");
		Serial1.println("AT+CMEE=2");
		do{
			delay(100);
			this->read_esp32SIM7600E();
			
		}while(buff.indexOf("OK") == -1 && check_uptime());
		
		Serial1.println("AT+CGREG?");
		do{
			delay(100);
			this->read_esp32SIM7600E();
			if(buff.indexOf("ERROR") != -1){
				return false;
			}
		}while(buff.indexOf("CGREG: 0,1") == -1 && check_uptime());


		Serial1.println("AT+NETCLOSE");
		this->read_esp32SIM7600E();
		delay(500);
		
		do{
			Serial1.println("AT+CGDCONT=1"",""\"IP\""",""\"Tim\""",""\"0.0.0.0\""",""0"",""0");
			delay(1000);
			this->read_esp32SIM7600E();
			
		}while(buff.indexOf("OK") == -1 && check_uptime());

		
		do{	
			Serial1.println("AT+CIPMODE=0");
			delay(100);
			this->read_esp32SIM7600E();
			
		}while(buff.indexOf("OK") == -1 && check_uptime());

		
		do{	
			Serial1.println("AT+CIPSENDMODE=0");
			delay(100);
			this->read_esp32SIM7600E();
			
		}while(buff.indexOf("OK") == -1 && check_uptime());


		
		do{	
			Serial1.println("AT+CIPCCFG=10,0,0,0,1,0,75000");
			delay(100);
			this->read_esp32SIM7600E();
			
		}while(buff.indexOf("OK") == -1 && check_uptime());

		
		do{	
			Serial1.println("AT+CIPTIMEOUT=75000,15000,15000");
			delay(100);
			this->read_esp32SIM7600E();
			
		}while(buff.indexOf("OK") == -1 && check_uptime());


		
		do{	
			Serial1.println("AT+NETOPEN");
			delay(100);
			this->read_esp32SIM7600E();
			
		}while(buff.indexOf("OK") == -1 && check_uptime());

		
		do{	
			Serial1.println("AT+IPADDR");
			delay(100);
			this->read_esp32SIM7600E();
			
		}while(buff.indexOf("OK") == -1 && check_uptime());

		
		
		do{	
			Serial1.println("AT+COPS?");
			delay(100);
			this->read_esp32SIM7600E();
			
		}while(buff.indexOf("TIM") == -1 && check_uptime());
	

return true;
}





bool esp32SIM7600E::register_device(){
	//String a = "{\"channel\":\"GPRS\",\"chipset\":\"EE:02:42:23:FA:5F\",\"mac\":\"9F:43:45:5F:F1:42\",\"name\":\"Esp32\",\"tag\":[\"iisc\"]}";
	String a = "{\"chipset\":\"Green1\",\"mac\":\"9F:43:45:5F:F1:42\",\"name\":\"GreenContainer\",\"tag\":[\"iisc\"]}";
	
	
	Serial1.println("AT+CHTTPACT=\"200.130.75.146\",80");
    delay(100);
	this->read_esp32SIM7600E();
    Serial1.println("POST /client HTTP/1.1");
	delay(100);
	this->read_esp32SIM7600E();
    Serial1.println("Connection: close");
	delay(100);
    this->read_esp32SIM7600E();
    Serial1.println("Host: 200.130.75.146");
	delay(100);
	this->read_esp32SIM7600E();
    Serial1.println("accept: application/json");
	delay(100);
    this->read_esp32SIM7600E();
    Serial1.println("Content-Type: application/json");
	delay(100);
    this->read_esp32SIM7600E();
	
    
    Serial1.print("Content-Length: ");
    Serial1.println(String(a.length()));
	//Serial1.println("90");
	delay(100);
    this->read_esp32SIM7600E();
    Serial1.println("");
    Serial1.println(a);
	delay(100);
	this->read_esp32SIM7600E();
    Serial1.println("");
	delay(100);
    Serial1.println(char(26));
	delay(5000);
	this->read_esp32SIM7600E();

	if(buff.indexOf("200") == -1){
		this->Sleep(300);

		return false;
	}


	Serial.println("foi");

  return true;
}
  

bool esp32SIM7600E::register_service(String unit,String parameter){
	int length1;

	Serial1.println("AT+CHTTPACT=\"200.130.75.146\",80");
    delay(100);
	this->read_esp32SIM7600E();
    Serial1.println("POST /service HTTP/1.1");
	delay(100);
	this->read_esp32SIM7600E();
    Serial1.println("Connection: close");
	delay(100);
    this->read_esp32SIM7600E();
    Serial1.println("Host: 200.130.75.146");
	delay(100);
    this->read_esp32SIM7600E();
    Serial1.println("Content-Type: application/json");
	delay(100);
    this->read_esp32SIM7600E();
    Serial1.print("Content-Length: ");
	length1 = unit.length() + parameter.length()+112;
    Serial1.println(String(length1));
	delay(100);
    this->read_esp32SIM7600E();
    Serial1.println("");
	delay(100);
    Serial1.print("{\"chipset\":\"Green1\",\"mac\":\"9F:43:45:5F:F1:42\",\"name");
	delay(100);
	this->read_esp32SIM7600E();
	Serial1.print("\":\"getRange\",\"number\":0,\"numeric\":0,\"parameter\":");
	delay(100);
	this->read_esp32SIM7600E();
	Serial1.print("\"" + parameter + "\",\"");
	Serial1.print("unit\":");
	delay(100);
	this->read_esp32SIM7600E();
	Serial1.println("\"" + unit + "\"}");
	delay(100);
	this->read_esp32SIM7600E();
    Serial1.println("");
    this->read_esp32SIM7600E();
    Serial1.println(char(26));
	delay(5000);
	this->read_esp32SIM7600E();
	if(buff.indexOf("200") == -1){
		this->Sleep(300);
		return false;
	}


  return true;
}

bool esp32SIM7600E::register_data(String data){
	
  	Serial1.println("AT+CHTTPACT=\"200.130.75.146\",80");
    delay(100);
	this->read_esp32SIM7600E();
    Serial1.println("POST /data HTTP/1.1");
	delay(100);
	this->read_esp32SIM7600E();
    Serial1.println("Connection: close");
	delay(100);
    this->read_esp32SIM7600E();
    Serial1.println("Host: 200.130.75.146");
	delay(100);
    this->read_esp32SIM7600E();
    Serial1.println("Content-Type: application/json");
	delay(100);
    this->read_esp32SIM7600E();
    
    Serial1.print("Content-Length: ");
    Serial1.println(String(94+data.length()));
	delay(100);
    this->read_esp32SIM7600E();
    Serial1.println("");
	 //Serial1.print("{\"tags\":[\"1\"],");
    Serial1.print("{\"tags\":[\"iisc\"],\"chipset\":\"Green1\",");
	delay(600);
	this->read_esp32SIM7600E();
	Serial1.print("\"mac\":\"9F:43:45:5F:F1:42\",\"serviceNumber\":0,\"value\":[\"" );
	delay(600);
	this->read_esp32SIM7600E();
	Serial1.print(data);
	delay(100);
	this->read_esp32SIM7600E();
    Serial1.println("\"]}");
	delay(100);
    this->read_esp32SIM7600E();
    Serial1.print(char(26));
	
	time0 = millis();
	while(Serial1.find("200") == false );
	time1 = millis();
	Serial.print(time1-time0);
	Serial.println(" ms");

	delay(5000);
	this->read_esp32SIM7600E();
	//Serial.println("post data");

	//Serial.println("sair");
	return true;
}

bool esp32SIM7600E::send_data (String data, String unit,String parameter){


	while( this->register_device() == false && check_uptime());
	delay(100);
	while( this->register_service(unit,parameter) == false && check_uptime());
	delay(100);
	while( this->register_data(data) == false && check_uptime());
	delay(100);
	//Serial1.end();
	//Serial.println("deu o post");

	while( this->post_rtt(String(time1-time0)) == false && check_uptime());
	return true;
}







void esp32SIM7600E::Sleep(unsigned long time_sleep){
	long time = millis();
	digitalWrite(LED_PIN, LOW);
	delay(500);
	digitalWrite(MODEM_FLIGHT, LOW);
	buff.remove(0,70); //Apagando buffer
	Serial1.println("AT+CPOF");
	delay(100);
	this->read_esp32SIM7600E();
	Serial.println("Deep sleep");
	esp_sleep_enable_timer_wakeup(time_sleep * 1000000ULL);	
	delay(200);
    esp_deep_sleep_start();

}

bool esp32SIM7600E::post_rtt(String rtt){
	Serial1.println("AT+CHTTPACT=\"200.130.75.146\",80");
    delay(100);
	this->read_esp32SIM7600E();
    Serial1.println("POST /data HTTP/1.1");
	delay(100);
    this->read_esp32SIM7600E();
    Serial1.println("Connection: close");
	delay(100);
    this->read_esp32SIM7600E();
    Serial1.println("Host: 200.130.75.146");
	delay(100);
    this->read_esp32SIM7600E();
    Serial1.println("Content-Type: application/json");
	delay(100);
    this->read_esp32SIM7600E();
    
    Serial1.print("Content-Length: ");
    Serial1.println(String(94+rtt.length()));
	delay(100);
    this->read_esp32SIM7600E();
    Serial1.println("");
	 //Serial1.print("{\"tags\":[\"1\"],");
    Serial1.print("{\"tags\":[\"rtt\"],\"chipset\":\"Green1\",");
	delay(600);
	this->read_esp32SIM7600E();
	Serial1.print("\"mac\":\"9F:43:45:5F:F1:42\",\"serviceNumber\":0,\"value\":[\"" );
	delay(600);
	this->read_esp32SIM7600E();
	Serial1.print(rtt);
	delay(100);
	this->read_esp32SIM7600E();
    Serial1.println("\"]}");
	delay(100);
    this->read_esp32SIM7600E();
    Serial1.print(char(26));
	delay(5000);
	this->read_esp32SIM7600E();


	if(buff.indexOf("200") == -1){
		return false;
	}
	
  	return true;
}



String esp32SIM7600E::getGPS(){
	
	
	double lat, longi;
	int cout = 0;
	
	Serial1.println("AT+CGPS=1");
	delay(100);
    this->read_esp32SIM7600E();

	Serial1.println("AT+CGPSINFOCFG=?");
	delay(100);
	this->read_esp32SIM7600E();

	do{
      Serial1.println("AT+CGNSSINFO");
      delay(100);
      this->read_esp32SIM7600E();
	  cout++;

	  if(cout == 100){

		Serial1.println("AT+CGPS=0");
		delay(100);
    	this->read_esp32SIM7600E();

		return "0,0";

	  }

      
    }while(buff.indexOf("W") == -1 && check_uptime());

	String gpsRx = buff;
	String lat1 = gpsRx.substring(38,40);
	String lat2 = gpsRx.substring(40,49);
	String long1 = gpsRx.substring(52,55);
	String long2 = gpsRx.substring(55,64);

	Serial1.println("AT+CGPS=0");
	delay(100);
    this->read_esp32SIM7600E();

	

	lat = (lat1.toFloat() + (lat2.toFloat()/60.000000))*-1.0;
	longi = (long1.toFloat() + (long2.toFloat()/60.00000))*-1.0;
  
	Serial.print(lat,6);
	Serial.print(",");
	Serial.println(longi,6);



  

  return String(lat,6)+ "," + String(longi,6);
}

float esp32SIM7600E::get_baterry(){
	float vbat;
	long time = millis();
	buff.remove(0,70);
	Serial1.println("AT+CBC");
		do{
			delay(100);
			this->read_esp32SIM7600E();
			
		}while(buff.indexOf("OK") == -1 && check_uptime());

	Serial.println(buff);
	buff = buff.substring(16,21);
	Serial.println(buff);
	return (buff.toFloat() - 3.5)*142.86;

}

