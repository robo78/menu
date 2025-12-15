# Firmware: Xiao ESP32-S3 + Wio-SX1262 + 2.0" ST7789V (240x320)

Ten katalog zawiera przykładowy firmware w Arduino/PlatformIO, który łączy mikrokontroler Seeed Studio Xiao ESP32-S3 z modemem LoRa Wio-SX1262 oraz wyświetlaczem TFT 2.0" ST7789V 240x320. Projekt demonstruje:

- inicjalizację i prosty ekran startowy na ST7789,
- konfigurację radia SX1262 (biblioteka RadioLib) i cykliczne wysyłanie komunikatu,
- współdzielenie jednej magistrali SPI dla radia i wyświetlacza.

## Wymagania
- PlatformIO (CLI lub w VS Code)
- Płytka: `seeed_xiao_esp32s3`
- Biblioteki: `Adafruit GFX`, `Adafruit ST7735 and ST7789`, `RadioLib`

## Schemat połączeń (tekstowy)
Wszystkie urządzenia pracują na jednej magistrali SPI. Linie zasilania (3V3, GND) pominięto dla czytelności.

### Wspólne sygnały SPI
| Sygnał | ESP32-S3 | ST7789V | Wio-SX1262 |
| --- | --- | --- | --- |
| SCK | GPIO6 (D5) | SCK | SCK |
| MOSI | GPIO7 (D6) | SDA/MOSI | MOSI |
| MISO | GPIO8 (D7) | (nieużywane) | MISO |

### Linie sterujące
| Funkcja | ESP32-S3 | ST7789V | Wio-SX1262 |
| --- | --- | --- | --- |
| CS (LCD) | GPIO5 (D4) | CS | — |
| DC (LCD) | GPIO4 (D3) | DC | — |
| RST (LCD) | GPIO3 (D2) | RST | — |
| BL (LCD) | GPIO2 (D1) | BL | — |
| CS (LoRa) | GPIO1 (D0) | — | NSS |
| RST (LoRa) | GPIO10 (D9) | — | NRESET |
| DIO1 (LoRa) | GPIO21 (D10) | — | DIO1 |
| BUSY (LoRa) | GPIO9 (D8) | — | BUSY |

> Uwagi: pin G9 (D8) w Xiao ESP32-S3 jest bezpieczny do użycia jako wejście/wyjście. Jeżeli używasz innej rewizji, zweryfikuj mapowanie pinów w dokumentacji Seeed.

### Prosty obraz połączeń
Mermaid pokazuje przebieg sygnałów; w podglądzie Markdown w VS Code/PlatformIO zostanie wygenerowany schemat.

```mermaid
graph LR
    subgraph SPI\n(shared)
    SCK((GPIO6/D5)) -- SCK --> ST7789SCK
    SCK -- SCK --> SX1262SCK
    MOSI((GPIO7/D6)) -- MOSI --> ST7789MOSI
    MOSI -- MOSI --> SX1262MOSI
    MISO((GPIO8/D7)) -- MISO --> SX1262MISO
    end

    subgraph LCD
    LCDCS((GPIO5/D4)) -- CS --> ST7789CS
    LCDDC((GPIO4/D3)) -- DC --> ST7789DC
    LCDRST((GPIO3/D2)) -- RST --> ST7789RST
    LCDBL((GPIO2/D1)) -- BL --> ST7789BL
    end

    subgraph LoRa
    LORACS((GPIO1/D0)) -- NSS --> SX1262CS
    LORARST((GPIO10/D9)) -- RESET --> SX1262RST
    LORADIO1((GPIO21/D10)) -- DIO1 --> SX1262DIO1
    LORABUSY((GPIO9/D8)) -- BUSY --> SX1262BUSY
    end
```

## Kompilacja i wgrywanie
1. Zainstaluj zależności: `pio pkg install` (opcjonalnie, biblioteki są zadeklarowane w `platformio.ini`).
2. Zbuduj: `pio run`.
3. Wgraj: `pio run -t upload` (upewnij się, że port szeregowy jest poprawnie wykryty).

## Konfiguracja radiowa
Domyślna częstotliwość to 868.0 MHz (EU868). W pliku `src/main.cpp` dostosuj `LORA_FREQ` oraz parametry `setBandwidth`, `setSpreadingFactor`, `setCodingRate` do wymagań lokalnych i prawnych.

## Plik źródłowy
Główna logika znajduje się w `src/main.cpp` i obejmuje:
- inicjalizację SPI dla LCD i LoRa,
- renderowanie ekranu powitalnego,
- rozpoczęcie pracy radia SX1262 i cykliczne wysyłanie ramki co 10 sekund,
- wyświetlanie statusu na LCD oraz przez port szeregowy.
