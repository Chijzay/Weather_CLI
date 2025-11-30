from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


@dataclass
class Location:
    name: str
    latitude: float
    longitude: float
    country: Optional[str] = None


@dataclass
class CurrentWeather:
    temperature: float
    windspeed: float
    winddirection: float
    weathercode: int


@dataclass
class DailyForecastDay:
    date: str
    temp_max: float
    temp_min: float
    precip_sum: float


@dataclass
class Forecast:
    location: Location
    current: CurrentWeather
    daily: List[DailyForecastDay]


class ApiError(RuntimeError):
    """Raised when the weather API or geocoding API fails."""


def geocode_city(name: str, country: Optional[str] = None) -> Location:
    """
    Look up a city using Open-Meteo's geocoding API.
    Returns a Location with coordinates, or raises ApiError / ValueError.
    """
    params = {
        "name": name,
        "count": 1,
        "language": "en",
        "format": "json",
    }
    if country:
        params["country"] = country

    try:
        response = requests.get(GEOCODING_URL, params=params, timeout=10)
    except requests.RequestException as exc:
        raise ApiError(f"Geocoding request failed: {exc}") from exc

    if not response.ok:
        raise ApiError(f"Geocoding API error: HTTP {response.status_code}")

    data = response.json()
    results = data.get("results") or []
    if not results:
        raise ValueError(f"No location found for '{name}'.")

    first = results[0]
    return Location(
        name=first.get("name", name),
        latitude=float(first["latitude"]),
        longitude=float(first["longitude"]),
        country=first.get("country"),
    )


def fetch_forecast(location: Location, days: int = 3) -> Forecast:
    """
    Fetch current weather and daily forecast for a given Location.
    `days` should be between 1 and 7 for this demo.
    """
    if days < 1:
        days = 1
    if days > 7:
        days = 7

    params = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "current_weather": "true",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": days,
    }

    try:
        response = requests.get(FORECAST_URL, params=params, timeout=10)
    except requests.RequestException as exc:
        raise ApiError(f"Forecast request failed: {exc}") from exc

    if not response.ok:
        raise ApiError(f"Forecast API error: HTTP {response.status_code}")

    data = response.json()

    current_raw = data.get("current_weather")
    if not current_raw:
        raise ApiError("Missing 'current_weather' in API response.")

    current = CurrentWeather(
        temperature=float(current_raw["temperature"]),
        windspeed=float(current_raw["windspeed"]),
        winddirection=float(current_raw["winddirection"]),
        weathercode=int(current_raw["weathercode"]),
    )

    daily_raw = data.get("daily") or {}
    times = daily_raw.get("time", [])
    tmax = daily_raw.get("temperature_2m_max", [])
    tmin = daily_raw.get("temperature_2m_min", [])
    rain = daily_raw.get("precipitation_sum", [])

    days_list: List[DailyForecastDay] = []
    for i in range(min(len(times), days)):
        days_list.append(
            DailyForecastDay(
                date=str(times[i]),
                temp_max=float(tmax[i]),
                temp_min=float(tmin[i]),
                precip_sum=float(rain[i]),
            )
        )

    return Forecast(location=location, current=current, daily=days_list)
