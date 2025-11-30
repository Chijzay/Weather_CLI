from __future__ import annotations

from weather_cli.formatter import (
    format_current,
    weather_code_to_description,
    weather_code_to_icon,
)
from weather_cli.api import CurrentWeather


def test_weather_code_to_icon_known_code():
    assert weather_code_to_icon(0) == "☀️"
    assert weather_code_to_icon(61) == "🌧️"
    assert weather_code_to_icon(95) == "⛈️"


def test_weather_code_to_icon_unknown_code():
    # some arbitrary unknown code
    assert weather_code_to_icon(999) == "❔"


def test_weather_code_to_description_basic_groups():
    assert weather_code_to_description(0) == "Clear sky"
    assert weather_code_to_description(2) == "Cloudy"
    assert weather_code_to_description(61) == "Rain"
    assert weather_code_to_description(71) == "Snow"
    assert weather_code_to_description(95) == "Thunderstorm"


def test_format_current_contains_temperature_and_icon():
    cw = CurrentWeather(
        temperature=12.345,
        windspeed=10.0,
        winddirection=180.0,
        weathercode=0,
    )
    text = format_current(cw)
    assert "12.3" in text  # rounded
    assert "☀️" in text
