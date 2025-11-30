from __future__ import annotations

from typing import Dict

from .api import CurrentWeather, DailyForecastDay, Forecast


def weather_code_to_icon(code: int) -> str:
    """
    Map WMO weather codes (used by Open-Meteo) to simple icons.
    This is a simplified mapping for demonstration purposes.
    """
    mapping: Dict[int, str] = {
        0: "☀️",   # Clear sky
        1: "🌤️",  # Mainly clear
        2: "⛅",   # Partly cloudy
        3: "☁️",   # Overcast
        45: "🌫️",  # Fog
        48: "🌫️",
        51: "🌦️",  # Drizzle
        53: "🌦️",
        55: "🌦️",
        61: "🌧️",  # Rain
        63: "🌧️",
        65: "🌧️",
        71: "🌨️",  # Snow
        73: "🌨️",
        75: "🌨️",
        80: "🌧️",  # Rain showers
        81: "🌧️",
        82: "🌧️",
        95: "⛈️",  # Thunderstorm
        96: "⛈️",
        99: "⛈️",
    }
    return mapping.get(code, "❔")


def weather_code_to_description(code: int) -> str:
    """
    Very small, human-readable description for some WMO codes.
    """
    if code == 0:
        return "Clear sky"
    if code in (1, 2, 3):
        return "Cloudy"
    if code in (45, 48):
        return "Fog"
    if code in (51, 53, 55, 61, 63, 65, 80, 81, 82):
        return "Rain"
    if code in (71, 73, 75):
        return "Snow"
    if code in (95, 96, 99):
        return "Thunderstorm"
    return f"Code {code}"


def format_current(current: CurrentWeather) -> str:
    icon = weather_code_to_icon(current.weathercode)
    desc = weather_code_to_description(current.weathercode)
    return (
        f"{current.temperature:.1f}°C, {desc} {icon}, "
        f"Wind {current.windspeed:.1f} km/h"
    )


def format_forecast_day(day: DailyForecastDay) -> str:
    return (
        f"{day.date}  "
        f"max {day.temp_max:4.1f}°C  "
        f"min {day.temp_min:4.1f}°C  "
        f"rain {day.precip_sum:4.1f} mm"
    )


def format_full_forecast(forecast: Forecast) -> str:
    """Return a multi-line string representation of the full forecast."""
    location_line = forecast.location.name
    if forecast.location.country:
        location_line += f", {forecast.location.country}"

    lines = [
        f"Location: {location_line}",
        f"Current:  {format_current(forecast.current)}",
        "",
        "Forecast:",
    ]
    if not forecast.daily:
        lines.append("  (no daily data)")
    else:
        for d in forecast.daily:
            lines.append(format_forecast_day(d))
    return "\n".join(lines)
