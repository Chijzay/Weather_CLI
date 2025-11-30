# Weather CLI mit Python

Weather CLI ist ein kleines Python-Befehlszeilenprogramm, das aktuelle Wetterdaten und eine Kurzvorhersage für eine Stadt oder Koordinaten abruft und dazu einfache Wetter-Icons wie ☀️, 🌧️, ⛈️, etc. ausgibt.

## Features

- Stadtname mit automatische Geocodierung (Open-Meteo Geocoding API)
- Wetterdaten und Tagesvorhersage (1–7 Tage)
- Ausgabe inklusive einfacher Wetter-Icons  
- Nutzung einer stabilen, keyless API  
- Test-Suite: `pytest`

# Schnellstart

## 1. Repository klonen

```bash
git clone https://github.com/Chijzay/Weather_CLI.git
cd Weather_CLI
```

## 2. Virtuelle Umgebung anlegen und aktivieren

Unter Windows:

```bash
python -m venv .venv
.venv\Scripts\Activate
```

## 3. Abhängigkeiten manuell installieren

```bash
python -m pip install requests pytest
```

## 4. Programm starten

Beispiele:

```bash
python main.py --city Berlin
python main.py --city "Hamburg"
python main.py --city "Paris" --country "France"
python main.py --lat 52.52 --lon 13.41
python main.py --city Berlin --days 5
```

Beispielausgabe:

```bash
Location: Hamburg, Germany
Current:  6.6°C, Cloudy ⛅, Wind 19.2 km/h

Forecast:
2025-11-30  max  9.6°C  min  5.0°C  rain  0.1 mm
2025-12-01  max  6.7°C  min  3.8°C  rain  0.0 mm
2025-12-02  max  5.8°C  min  3.6°C  rain  1.1 mm
```

# Projektstruktur

```
weather-cli/
├── README.md              # Projektdokumentation
├── main.py                # Einstiegspunkt
├── weather_cli
│   ├── __init__.py        # Paket-Markierung
│   ├── cli.py             # CLI-Logik (Argumente, Ablauf)
│   ├── api.py             # API-Aufrufe (Open-Meteo)
│   └── formatter.py       # Formatierung, Icons, Textausgabe
└── tests
    └── test_formatter.py  # Beispieltests
```

