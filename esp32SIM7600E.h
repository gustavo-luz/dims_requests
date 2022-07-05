#ifndef SAIDA_H
#define SAIDA_H

#include <Arduino.h>



#endif

#ifndef esp32SIM7600E_H
#define esp32SIM7600E_H

class esp32SIM7600E {
    public:
        esp32SIM7600E();
        bool init();
        bool connect();
        void reboot();
		bool check_uptime();
        void read_esp32SIM7600E();
        bool send_data (String,String,String);
        bool register_device();
        float get_baterry();
        bool register_service(String,String);
        bool register_data(String);
        void (*funcReset) () = 0;
        void Sleep(unsigned long);
        void wake_up();
        bool any_get(String url,String dir);
        bool post_rtt(String);
        String getGPS();
    private:
		
        


};
#endif

