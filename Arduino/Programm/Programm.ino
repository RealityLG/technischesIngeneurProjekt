#include <SPI.h>
#include <MFRC522.h>
#include <Adafruit_NeoPixel.h>

// RFID Pins
#define SS_PIN 10
#define RST_PIN 9

// Ultraschall Pins
#define TRIG_PIN 6
#define ECHO_PIN 7

// LED-Leiste
#define LED_PIN 8
#define NUM_LEDS 8  // 8 LEDs auf deiner Leiste

MFRC522 mfrc522(SS_PIN, RST_PIN);
Adafruit_NeoPixel strip(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

unsigned long cooldownStart = 0;
const unsigned long cooldownTime = 15000; // 15 Sekunden
bool cooldownActive = false;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // RFID Setup
  SPI.begin();
  mfrc522.PCD_Init();

  // Ultraschall Setup
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // LED-Leiste Setup
  strip.begin();
  strip.show(); // Alle LEDs aus

  Serial.println(F("RFID + Ultraschall + LED System gestartet"));
  Serial.println(F("Karte auflegen zum Einchecken"));
}

void loop() {
  // Ultraschall-Messung (läuft immer)
  long distance = measureDistance();
  updateLEDs(distance);

  // RFID Code (wie vorher)
  if (cooldownActive) {
    unsigned long elapsed = millis() - cooldownStart;
    unsigned long remaining = cooldownTime - elapsed;

    static unsigned long lastPrint = 0;
    if (millis() - lastPrint >= 1000) {
      lastPrint = millis();
      Serial.print(F("Cooldown aktiv: "));
      Serial.print(remaining / 1000);
      Serial.println(F(" Sekunden verbleibend"));
    }

    if (elapsed >= cooldownTime) {
      cooldownActive = false;
      Serial.println(F("Cooldown vorbei - neue Karten können gescannt werden."));
    }
    return;
  } else {

    if (!mfrc522.PICC_IsNewCardPresent()) return;
    if (!mfrc522.PICC_ReadCardSerial()) return;

    String uid = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      if (mfrc522.uid.uidByte[i] < 0x10) uid += "0";
      uid += String(mfrc522.uid.uidByte[i], HEX);
    }
    uid.toUpperCase();

    Serial.print(F("Karte erkannt! UID: "));
    Serial.println(uid);

    cooldownStart = millis();
    cooldownActive = true;

    mfrc522.PICC_HaltA();
    mfrc522.PCD_StopCrypto1();
  }
}

long measureDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  long duration = pulseIn(ECHO_PIN, HIGH);
  long distance = duration * 0.034 / 2;
  
  return distance;
}

void updateLEDs(long distance) {
  uint32_t color;
  
  if (distance > 100) {          // > 1m = GRÜN
    color = strip.Color(0, 255, 0);
  } 
  else if (distance >= 50) {     // 50cm - 1m = ORANGE
    color = strip.Color(255, 165, 0);
  } 
  else {                         // < 50cm = ROT
    color = strip.Color(255, 0, 0);
  }
  
  // Alle 8 LEDs auf die Farbe setzen
  for(int i = 0; i < 8; i++) {
    strip.setPixelColor(i, color);
  }
  strip.show();
  
  // Debug-Ausgabe nur alle 2 Sekunden
  static unsigned long lastDistancePrint = 0;
  if (millis() - lastDistancePrint >= 2000) {
    lastDistancePrint = millis();
    Serial.print(F("Entfernung: "));
    Serial.print(distance);
    Serial.print(F(" cm - "));
    if (distance > 100) Serial.println(F("GRÜN"));
    else if (distance >= 50) Serial.println(F("ORANGE"));
    else Serial.println(F("ROT"));
  }
  
  delay(100); // Kleine Pause zwischen Messungen
}