//Vincent
#include <SPI.h>
#include <MFRC522.h>
#include <Adafruit_NeoPixel.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <RTClib.h>
DateTime checkInTime; // <--- Diese Zeile hinzufügen!


//Vincent
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

//serhat
RTC_DS1307 rtc;
LiquidCrystal_I2C lcd(0x27, 16, 2);


//vincent
unsigned long cooldownStart = 0;
const unsigned long cooldownTime = 15000; // 15 Sekunden
bool cooldownActive = false;

bool position = false; //false = frei, true = belegt
DateTime parkStartTime; 
/*
Skript.ino
Arduino Skript für Sensoren und LED-Steuerung
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


  lcd.init();
  lcd.backlight();
  lcd.clear();

  if(!rtc.begin()) {
    Serial.println("RTC nicht gefunden!");
    while(1);
  }
  if(!rtc.isrunning()) {
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
  
  //Vincent
  Serial.println(F("RFID + Ultraschall + LED + RTC System gestartet"));
  Serial.println(F("Karte auflegen zum Einchecken"));
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Parksystem");
}

unsigned long lastPrint = 0;
void loop() {
  // Ultraschall-Messung
  long distance = measureDistance();
  updateLEDs(distance);

  ///Cooldown runterzählen
  if (cooldownActive) {

    //millis() verstrichene Zeit seit Start von Controller
    //timePassed = wie viel Zeit seit Cooldownstart vergangen ist
    unsigned long timePassed = millis() - cooldownStart;
    //übrige Zeit
    unsigned long remaining = cooldownTime - timePassed;

    if (millis() - lastPrint >= 1000) {
      lastPrint = millis();
      Serial.print(F("Cooldown aktiv: "));
      Serial.print(remaining / 1000);
      Serial.println(F(" Sekunden verbleibend"));
    }

    if (timePassed >= cooldownTime) {
      cooldownActive = false;
      Serial.println(F("Cooldown vorbei - neue Karten können gescannt werden."));
    }
    return;

  } else {

    // Überprüfung ob Karte vorhanden ist
    if (!mfrc522.PICC_IsNewCardPresent()) return;
    if (!mfrc522.PICC_ReadCardSerial()) return;

    String uid = "";
    //Stuct mfrc522.uid gegeben
    /*
        size
        uidByte[]
        sak (Kartentyp)
    */
    for (byte i = 0; i < mfrc522.uid.size; i++) {

      if (mfrc522.uid.uidByte[i] < 0x10) uid += "0";
      //wandelt uidByte in Hex um, HEX bestimmt Format
      uid += String(mfrc522.uid.uidByte[i], HEX);
    }
    uid.toUpperCase();

    Serial.print(F("Karte erkannt! UID: "));
    
    //Posiion aktualisieren
    //Serhat
    position = !position;
  
    display(position);
    //Vincent
    Serial.println(uid);
    

    cooldownStart = millis();
    cooldownActive = true;
    //für Cooldown Ausgabe pro Sekunde
    lastPrint = 0;

    mfrc522.PICC_HaltA();
    mfrc522.PCD_StopCrypto1();
  }

  leddim();
}
