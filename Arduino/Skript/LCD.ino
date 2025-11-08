#include <Wire.h>
#include <RTClib.h>
#include <LiquidCrystal_I2C.h>

/*
von Serhat Subasi
Matrikelnummer: 327488
*/



// Zugriff auf globale Variablen
extern RTC_DS1307 rtc;
extern LiquidCrystal_I2C lcd;
extern DateTime checkInTime;

void display(bool position) {
  lcd.clear();       //räumt den Bildschirm auf


  if (position) {
    // Einchecken
    checkInTime = rtc.now();
    lcd.setCursor(0, 0);      // setzt auf die erste Zeile erste spalte auf dem Display
    lcd.print("Es wurde");    // gibt den Text auf dem LCD Modul aus
    lcd.setCursor(0, 1);      // setzt auf die zweite Zeile
    lcd.print("Eingecheckt!");
    Serial.println(F("Es wurde eingecheckt"));
  }
  else {
    // === Auschecken ===
    DateTime checkOutTime = rtc.now();                // holt die aktuelle Zeit
    TimeSpan parkdauer = checkOutTime - checkInTime;  // berechnet die Parkdauer durch die Differenz

    lcd.setCursor(0, 0);
    lcd.print("Es wurde");
    lcd.setCursor(0, 1);
    lcd.print("ausgecheckt");

    delay(2000); // 2 Sekunden Pause, bevor die Parkdauer angezeigt wird
    lcd.clear();

    lcd.setCursor(0, 0);
    lcd.print("Parkdauer:");
    lcd.setCursor(0, 1);
    lcd.print(parkdauer.hours());    // gibt die Stunde aus
    lcd.print("h ");
    lcd.print(parkdauer.minutes());  // gibt die Minute aus
    lcd.print("m");

    Serial.print(F("Es wurde ausgecheckt - Parkdauer: "));
    Serial.print(parkdauer.hours());
    Serial.print(" Stunden, ");
    Serial.print(parkdauer.minutes());
    Serial.println(" Minuten");
  }
}