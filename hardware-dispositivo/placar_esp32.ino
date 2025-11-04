
// --- Bibliotecas
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// --- Configurações de Rede
const char* SSID = "Wokwi-GUEST";
const char* PASSWORD = "";

// --- Configurações do MQTT 
const char* BROKER_MQTT = "54.221.163.3"; // IP do professor
const int BROKER_PORT = 1883;

const char* ID_MQTT = "esp32_placar_01";
const char* TOPICO_PUBLISH_A = "passa-a-bola/timeA/attrs";
const char* TOPICO_PUBLISH_B = "passa-a-bola/timeB/attrs";
const char* TOPICO_SUBSCRIBE = "passa-a-bola/baliza01/cmd";

// --- Pinos e Componentes
const int I2C_SDA_PIN = 21;
const int I2C_SCL_PIN = 22;
const int BUZZER_PIN = 19;
const int TRIG_PIN_A = 5;
const int ECHO_PIN_A = 18;
const int TRIG_PIN_B = 16;
const int ECHO_PIN_B = 17;
LiquidCrystal_I2C lcd(0x27, 16, 2); 
WiFiClient espClient;
PubSubClient MQTT(espClient);
int gols_A = 0;
int gols_B = 0;
bool bolaDetectada_A = false;
bool bolaDetectada_B = false;

// --- Funções de Inicialização

void initSerial() { Serial.begin(115200); }
void initLCD() {
  Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);
  lcd.init(); lcd.backlight();
  lcd.setCursor(0, 0); lcd.print("A:0 B:0");
  lcd.setCursor(0, 1); lcd.print("Conectando...");
}
void initPins() {
  pinMode(TRIG_PIN_A, OUTPUT); pinMode(ECHO_PIN_A, INPUT);
  pinMode(TRIG_PIN_B, OUTPUT); pinMode(ECHO_PIN_B, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
}
void initWiFi() {
  Serial.print("Conectando-se ao WiFi...");
  WiFi.begin(SSID, PASSWORD);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\nWiFi conectado!");
  lcd.clear();
  lcd.setCursor(0, 0); lcd.print("A:0 B:0");
  lcd.setCursor(0, 1); lcd.print("WiFi Conectado!");
}

// --- Callback
void mqtt_callback(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (int i = 0; i < length; i++) msg += (char)payload[i];
  Serial.print("Mensagem recebida ["); Serial.print(topic); Serial.print("]: "); Serial.println(msg);
  StaticJsonDocument<128> doc;
  deserializeJson(doc, msg);
  const char* comando = doc["comando"]; 
  if (strcmp(comando, "resetar") == 0) {
    Serial.println("Comando de RESET recebido!");
    lcd.clear();
    lcd.setCursor(0, 0);
    if (gols_A > gols_B) { lcd.print("Time A Venceu!"); }
    else if (gols_B > gols_A) { lcd.print("Time B Venceu!"); }
    else { lcd.print("Empate!"); }
    lcd.setCursor(0, 1);
    lcd.print("Final: "); lcd.print(gols_A); lcd.print(" a "); lcd.print(gols_B);
    delay(3000);
    gols_A = 0; 
    gols_B = 0;
    lcd.clear();
    lcd.setCursor(0, 0); lcd.print("A:0 B:0");
    lcd.setCursor(0, 1); lcd.print("WiFi Conectado!");
  }
}

// --- Funções MQTT
void initMQTT() {
  MQTT.setServer(BROKER_MQTT, BROKER_PORT);
  MQTT.setCallback(mqtt_callback); 
}
void reconnectMQTT() {
  while (!MQTT.connected()) {
    Serial.print("Conectando ao Broker MQTT...");
    if (MQTT.connect(ID_MQTT)) {
      Serial.println("Conectado!");
      MQTT.subscribe(TOPICO_SUBSCRIBE);
      Serial.print("Subscrito em: "); Serial.println(TOPICO_SUBSCRIBE);
    } else {
      Serial.print("Falha (rc="); Serial.print(MQTT.state()); Serial.println("), tentando novamente em 2s...");
      delay(2000);
    }
  }
}
void VerificaConexoesWiFIEMQTT() {
  if (WiFi.status() != WL_CONNECTED) initWiFi(); 
  if (!MQTT.connected()) reconnectMQTT();     
}
void sendDataMQTT(const char* topico, int totalGols, const char* timeID) {
  StaticJsonDocument<128> doc;
  doc["gols"] = totalGols;
  doc["sensor_id"] = timeID;
  doc["timestamp"] = millis(); 
  char buffer[128];
  serializeJson(doc, buffer);
  MQTT.publish(topico, buffer);
  Serial.print("--- GOL PUBLICADO ("); Serial.print(timeID); Serial.print(") ---");
  Serial.println(buffer);
}
int lerSensor(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW); delayMicroseconds(2);
  digitalWrite(trigPin, HIGH); delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);
  return duration * 0.034 / 2;
}

// ===== SETUP
void setup() {
  initSerial();
  initPins();
  initLCD();
  initWiFi();
  initMQTT();
}

// ===== LOOP
void loop() {
  VerificaConexoesWiFIEMQTT(); 
  MQTT.loop(); 

  int distance_A = lerSensor(TRIG_PIN_A, ECHO_PIN_A);
  if (distance_A < 10 && !bolaDetectada_A) {
    bolaDetectada_A = true;
    gols_A++;
    Serial.print("GOLO TIME A! Total: "); Serial.println(gols_A);
    lcd.setCursor(0, 0);
    lcd.print("A:"); lcd.print(gols_A); lcd.print(" B:"); lcd.print(gols_B); 
    
    tocarSomGolOle(0);
    
    sendDataMQTT(TOPICO_PUBLISH_A, gols_A, "timeA");
    delay(1000); 
  }
  if (distance_A > 15) { bolaDetectada_A = false; }

  int distance_B = lerSensor(TRIG_PIN_B, ECHO_PIN_B);
  if (distance_B < 10 && !bolaDetectada_B) {
    bolaDetectada_B = true;
    gols_B++;
    Serial.print("GOLO TIME B! Total: "); Serial.println(gols_B);
    lcd.setCursor(0, 0);
    lcd.print("A:"); lcd.print(gols_A); lcd.print(" B:"); lcd.print(gols_B); 
    

    tocarSomGolOle(1);
    
    sendDataMQTT(TOPICO_PUBLISH_B, gols_B, "timeB");
    delay(1000); 
  }
  if (distance_B > 15) { bolaDetectada_B = false; }

  delay(100); 
}

void tocarSomGolOle(int tom) {

  
  int nota_baixa = (tom == 0) ? 392 : 440; // Tom 0 = G4, Tom 1 = A4
  int nota_alta  = (tom == 0) ? 440 : 494; // Tom 0 = A4, Tom 1 = B4

  
  int duracao_curta = 150;
  int duracao_longa = 250;
  int pausa = 50;


  tone(BUZZER_PIN, nota_baixa, duracao_curta);
  delay(duracao_curta + pausa);
  tone(BUZZER_PIN, nota_alta, duracao_longa);
  delay(duracao_longa + pausa + 100);

 
  tone(BUZZER_PIN, nota_baixa, duracao_curta);
  delay(duracao_curta + pausa);
  tone(BUZZER_PIN, nota_alta, duracao_longa);
  delay(duracao_longa);
  
}