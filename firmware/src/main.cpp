#include <Arduino.h>
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7789.h>
#include <RadioLib.h>

// --- Pin map ---
// SPI shared bus
constexpr int TFT_SCK = 6;   // D5
constexpr int TFT_MOSI = 7;  // D6
constexpr int TFT_MISO = 8;  // D7 (LCD nie używa, ale wymagany przez SPI)
constexpr int LORA_SCK = TFT_SCK;
constexpr int LORA_MOSI = TFT_MOSI;
constexpr int LORA_MISO = TFT_MISO;

// TFT control
constexpr int TFT_CS = 5;   // D4
constexpr int TFT_DC = 4;   // D3
constexpr int TFT_RST = 3;  // D2
constexpr int TFT_BL = 2;   // D1

// SX1262 control
constexpr int LORA_CS = 1;    // D0
constexpr int LORA_RST = 10;  // D9
constexpr int LORA_DIO1 = 21; // D10 (wejście przerwania)
constexpr int LORA_BUSY = 9;  // D8

#ifndef LORA_FREQ
#define LORA_FREQ 868.0
#endif

SPIClass sharedSPI(FSPI);
Adafruit_ST7789 tft(&sharedSPI, TFT_CS, TFT_DC, TFT_RST);
SX1262 radio = new Module(LORA_CS, LORA_DIO1, LORA_RST, LORA_BUSY);

uint32_t lastSend = 0;
const uint32_t sendIntervalMs = 10'000;

void drawSplash(const char* statusText) {
  tft.fillScreen(ST77XX_BLACK);
  tft.setTextColor(ST77XX_WHITE);
  tft.setTextSize(2);
  tft.setCursor(10, 20);
  tft.println("XIAO ESP32-S3");
  tft.setTextSize(1);
  tft.println("Wio-SX1262 + ST7789V");
  tft.println("Demo firmware");

  tft.setCursor(10, 100);
  tft.setTextColor(ST77XX_CYAN);
  tft.setTextSize(2);
  tft.println("Status:");
  tft.setTextSize(1);
  tft.setTextColor(ST77XX_YELLOW);
  tft.println(statusText);
}

void appendLog(const String& line) {
  Serial.println(line);
  tft.fillRect(0, 180, 240, 140, ST77XX_BLACK);
  tft.setCursor(10, 180);
  tft.setTextColor(ST77XX_GREEN);
  tft.setTextSize(1);
  tft.print("Last: ");
  tft.println(line);
}

void setup() {
  pinMode(TFT_BL, OUTPUT);
  digitalWrite(TFT_BL, HIGH);

  Serial.begin(115200);
  delay(200);

  // Start shared SPI (LCD first to get splash screen quickly)
  sharedSPI.begin(TFT_SCK, TFT_MISO, TFT_MOSI, TFT_CS);

  tft.init(240, 320);
  tft.setRotation(2); // zależnie od montażu można zmienić na 0-3
  drawSplash("Inicjalizacja...");

  // Konfiguracja radia SX1262
  radio.setSPI(&sharedSPI);
  int state = radio.begin(LORA_FREQ);
  if (state == RADIOLIB_ERR_NONE) {
    radio.setBandwidth(125.0);
    radio.setSpreadingFactor(7);
    radio.setCodingRate(5);
    radio.setOutputPower(14);
    appendLog("Radio OK @" + String(LORA_FREQ, 1) + "MHz");
  } else {
    appendLog("Radio error: " + String(state));
  }
}

void loop() {
  if (millis() - lastSend >= sendIntervalMs) {
    lastSend = millis();
    String payload = "HELLO @" + String(lastSend);

    int state = radio.transmit(payload);
    if (state == RADIOLIB_ERR_NONE) {
      appendLog("TX OK: " + payload);
    } else {
      appendLog("TX fail: " + String(state));
    }
  }
}
