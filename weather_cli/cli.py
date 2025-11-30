from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from .api import ApiError, Location, fetch_forecast, geocode_city
from .formatter import format_full_forecast


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simple CLI tool to fetch current weather and a short forecast."
    )
    parser.add_argument(
        "--city",
        type=str,
        help="City name (e.g. 'Berlin').",
    )
    parser.add_argument(
        "--country",
        type=str,
        help="Optional country name (e.g. 'Germany'). Used to disambiguate cities.",
    )
    parser.add_argument(
        "--lat",
        type=float,
        help="Latitude (used instead of --city).",
    )
    parser.add_argument(
        "--lon",
        type=float,
        help="Longitude (used instead of --city).",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=3,
        help="Number of forecast days (1–7). Default: 3",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print extra information (e.g. resolved coordinates).",
    )
    return parser.parse_args(argv)


def resolve_location(args: argparse.Namespace) -> Location:
    if args.city:
        return geocode_city(args.city, country=args.country)

    if args.lat is not None and args.lon is not None:
        return Location(
            name=f"{args.lat:.2f},{args.lon:.2f}",
            latitude=args.lat,
            longitude=args.lon,
            country=None,
        )

    print("You must provide either --city or both --lat and --lon.", file=sys.stderr)
    sys.exit(1)


def main(argv: Optional[list[str]] = None) -> None:
    args = parse_args(argv)

    try:
        location = resolve_location(args)
    except (ApiError, ValueError) as exc:
        print(f"Error resolving location: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        loc_line = location.name
        if location.country:
            loc_line += f", {location.country}"
        print(
            f"Resolved location: {loc_line} "
            f"({location.latitude:.4f}, {location.longitude:.4f})"
        )

    try:
        forecast = fetch_forecast(location, days=args.days)
    except ApiError as exc:
        print(f"Error fetching forecast: {exc}", file=sys.stderr)
        sys.exit(1)

    print(format_full_forecast(forecast))
