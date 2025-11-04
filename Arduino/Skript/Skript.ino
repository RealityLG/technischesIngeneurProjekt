#include <SPI.h>
#include <MFRC522.h>
#include <Adafruit_NeoPixel.h>

// RFID
#define SS_PIN 10
#define RST_PIN 9


// Ultraschall
#define TRIG_PIN 6
#define ECHO_PIN 7


// LED-Leiste
#define LED_PIN 8
#define NUM_LEDS 8  // 8 LEDs auf der Leiste

MFRC522 mfrc522(SS_PIN, RST_PIN);
Adafruit_NeoPixel strip(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

unsigned long cooldownStart = 0;
const unsigned long cooldownTime = 15000; // 15 Sekunden
bool cooldownActive = false;
bool position = false; //für Anzeige
/*
Skript.ino
Datenbankfunktionen für Parkplatzverwaltungssystem
@author: Vincent Gentz
Matrikelnummer:
Datum: 22.10.2025"""
*/

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
  //strip.setBrightness(30);

  Serial.println(F("RFID + Ultraschall + LED System gestartet"));
  Serial.println(F("Karte auflegen zum Einchecken"));

}

void loop() {
  // Ultraschall-Messung
  long distance = measureDistance();
  updateLEDs(distance);

  ///Cooldown runterzählen
  if (cooldownActive) {

    //millis() verstrichene Zeit seit Start von Controller
    //elapsed = wie viel Zeit seit Cooldownstart vergangen ist
    unsigned long elapsed = millis() - cooldownStart;
    //übrige Zeit
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
    
    //Posiion aktualisieren
    if(!position) {
      position = true;
      //Serial.println("True");
    } else {
      position = false;
      //Serial.println("False");
    }

    Serial.println(uid);

    cooldownStart = millis();
    cooldownActive = true;

    mfrc522.PICC_HaltA();
    mfrc522.PCD_StopCrypto1();
  }
}

