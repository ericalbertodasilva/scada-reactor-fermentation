#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

/*DHT22*/
#define DHTPIN 5  //Pino do DHT22
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT _dht(DHTPIN, DHTTYPE);
struct DHTdata {
  float t; //temperatura
  float h; //umidade do ar
};

// Sensores dos contadores de gas
int sensor1 = 2, sensor2 = 3;
int receberSensor1[4];
int receberSensor2[4];
int cont1, cont2;

/*Comunicacao serial*/
const byte NUMCHARS = 64;
char _receivedChars[NUMCHARS];
boolean _newMsgReceived = false;

DHTdata readDht(){
  DHTdata data;
  data.t = _dht.readTemperature();
  data.h = _dht.readHumidity();
  //verifica se resultados sao validos
  if (isnan(data.t) || isnan(data.h)) {
      data.h = -1;
      data.t = -1;
  } 
  return(data);
}

void sendAllData(){
  DHTdata data = readDht();             //le temperatura e umidade
  
  //<a;temperatura;UR;sensor1;sensor2>
  String s = "<a;"+String(data.t,2)+";"+String(data.h,2)+";"+String(cont1)+";"+String(cont2)+">";
  Serial.println(s);
}

/*
 * Atencao: Duas variaveis static... algumas vezes nem toda a mensagem chega 
 * de uma vez. É possível compor a mensagem em mais do que um ciclo do loop
*/
void getSerialMessage() {
  static boolean recvInProgress = false;
  static byte j = 0;
  char startMarker = '<';
  char endMarker = '>';
  char c;

  while (Serial.available() > 0 && _newMsgReceived == false) {
    c = Serial.read();

    if (recvInProgress == true) {
      if (c != endMarker) {
        _receivedChars[j] = c;
        j++;
        if (j >= NUMCHARS) {
            j = NUMCHARS - 1;
        }
      } else {
        _receivedChars[j] = '\0'; // terminate the string
        recvInProgress = false;
        j = 0;
        _newMsgReceived = true;
      }
    }

    else if (c == startMarker) {
      recvInProgress = true;
    }
  }
}

void zerarReator1() {
  cont1 = 0;
  Serial.println("<b>");
}

void zerarReator2() {
  cont2 = 0;
  Serial.println("<c>");
}

void decodeRequest()
{    
  String s;

  char cmd = _receivedChars[0];

  switch(cmd)
  {
    case '?': //echo
      Serial.println("<?>");
      break;

    case 'a': //envia string com varias informacoes para monitoramento do sistema
      sendAllData();
      break;
    
    case 'b': //envia string com varias informacoes para monitoramento do sistema
      zerarReator1();
      break;
    
    case 'c': //envia string com varias informacoes para monitoramento do sistema
      zerarReator2();
      break;

    default:
      Serial.println("<?>");
      break;
  }    
}

// the setup routine runs once when you press reset:
void setup() {
  _dht.begin();
  // initialize serial communication at 9600 bits per second:
  Serial.begin(115200);
  // make the pushbutton's pin an input:
  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);
}

// the loop routine runs over and over again forever:
void loop() {
  //Monitora serial  
  getSerialMessage();
  if (_newMsgReceived == true) {      
      decodeRequest();    
      _newMsgReceived = false;
  }
  receberSensor1[3] = receberSensor1[2];
  receberSensor1[2] = receberSensor1[1];
  receberSensor1[1] = receberSensor1[0];
  receberSensor1[0] = digitalRead(sensor1);
  receberSensor2[3] = receberSensor2[2];
  receberSensor2[2] = receberSensor2[1];
  receberSensor2[1] = receberSensor2[0];
  receberSensor2[0] = digitalRead(sensor2);
  if ((receberSensor1[0] == 0) && (receberSensor1[1] == 0) && (receberSensor1[2] == 1) && (receberSensor1[3] == 1)){
    cont1 = cont1 + 1;
  }
  if ((receberSensor2[0] == 0) && (receberSensor2[1] == 0) && (receberSensor2[2] == 1) && (receberSensor2[3] == 1)){
    cont2 = cont2 + 1;
  }
}
