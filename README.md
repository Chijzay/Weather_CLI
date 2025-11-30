# Weather CLI mit Python

Weather CLI ist ein kleines Python-Befehlszeilenprogramm, das aktuelle Wetterdaten und eine Kurzvorhersage für eine Stadt oder Koordinaten abruft und dazu einfache Wetter-Icons wie ☀️, 🌧️, ⛈️, etc. ausgibt.

## Features

- Stadtname mit automatische Geocodierung (Open-Meteo Geocoding API)
- Wetterdaten und Tagesvorhersage (1–7 Tage)
- Ausgabe inkl. einfacher Wetter-Icons  
- Nutzung einer stabilen, keyless API  
- Nur 1 externe Abhängigkeit: `requests`
- Test-Suite: `pytest`

# Schnellstart

## 1. Repository klonen

```bash
git clone https://github.com/Chijzay/Weather_CLI.git
cd weather-cli
