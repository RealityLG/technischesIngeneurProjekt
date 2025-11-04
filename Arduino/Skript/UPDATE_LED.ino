#include <SPI.h>
#include <MFRC522.h>
#include <Adafruit_NeoPixel.h>


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
