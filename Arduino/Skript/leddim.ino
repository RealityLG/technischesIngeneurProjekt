#include <Adafruit_NeoPixel.h>
#include <RTClib.h>

/*
von Serhat Subasi
Matrikelnummer: 327488
*/



// Zugriff auf globale Variablen
extern RTC_DS1307 rtc;
extern Adafruit_NeoPixel strip;


void leddim() {
  DateTime now = rtc.now();   // aktuelle Zeit abrufen
  int stunde = now.hour();

  // Debug-Ausgabe
  Serial.print(F("Aktuelle Uhrzeit: "));
  Serial.print(stunde);
  Serial.print(F(":"));
  Serial.println(now.minute());

  // --- Nachtmodus prüfen ---
  if (stunde >= 20 || stunde < 8) {   //prüft ob es zwischen 20 und 8 Uhr ist
    strip.setBrightness(40);  // Helligkeit reduzieren (0–255)
  } else {
    strip.setBrightness(150); // Helligkeit erhöhen
  }

  strip.show(); // Änderungen übernehmen
}