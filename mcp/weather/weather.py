from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")

GEOCODING_API = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_API = "https://api.open-meteo.com/v1/forecast"

# WMO weather interpretation codes (subset)
WMO_DESCRIPTIONS: dict[int, str] = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


async def api_get(url: str, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def weather_description(code: int) -> str:
    return WMO_DESCRIPTIONS.get(code, f"Weather code {code}")


async def resolve_city(city: str, country_code: str = "") -> dict[str, Any] | None:
    """Resolve a European city name to coordinates via Open-Meteo geocoding."""
    params: dict[str, Any] = {"name": city, "count": 1, "language": "en"}
    if country_code:
        params["country_code"] = country_code.upper()

    data = await api_get(GEOCODING_API, params)
    if not data or not data.get("results"):
        return None
    return data["results"][0]


def location_label(location: dict[str, Any]) -> str:
    parts = [location["name"]]
    if admin1 := location.get("admin1"):
        parts.append(admin1)
    if country := location.get("country"):
        parts.append(country)
    return ", ".join(parts)


@mcp.tool()
async def get_weather_advisories(city: str, country_code: str = "") -> str:
    """Get weather advisories for a European city based on the next few days' forecast.

    Args:
        city: City name (e.g. Paris, Berlin, Rome)
        country_code: Optional ISO 3166-1 alpha-2 country code to disambiguate (e.g. FR, DE, IT)
    """
    location = await resolve_city(city, country_code)
    if not location:
        hint = f" Try adding country_code (e.g. FR for {city})." if not country_code else ""
        return f"Could not find city '{city}'.{hint}"

    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max",
        "timezone": "auto",
        "forecast_days": 3,
    }
    data = await api_get(FORECAST_API, params)
    if not data or "daily" not in data:
        return f"Unable to fetch advisory data for {location_label(location)}."

    daily = data["daily"]
    advisories: list[str] = []
    label = location_label(location)

    for i, date in enumerate(daily["time"]):
        notes: list[str] = []
        precip = daily["precipitation_sum"][i]
        wind = daily["windspeed_10m_max"][i]
        t_max = daily["temperature_2m_max"][i]
        t_min = daily["temperature_2m_min"][i]
        code = daily["weathercode"][i]

        if precip >= 20:
            notes.append(f"heavy rain expected ({precip} mm)")
        elif precip >= 5:
            notes.append(f"rain expected ({precip} mm)")
        if wind >= 60:
            notes.append(f"strong winds (up to {wind} km/h)")
        elif wind >= 40:
            notes.append(f"windy (up to {wind} km/h)")
        if t_max >= 35:
            notes.append(f"heat advisory (high {t_max}°C)")
        if t_min <= 0:
            notes.append(f"freezing conditions (low {t_min}°C)")
        if code in (95, 96, 99):
            notes.append("thunderstorms possible")

        if notes:
            advisories.append(f"{date}: {', '.join(notes).capitalize()}")

    if not advisories:
        return f"No significant weather advisories for {label} in the next 3 days."

    return f"Advisories for {label}:\n\n" + "\n".join(advisories)


@mcp.tool()
async def get_forecast(city: str, country_code: str = "") -> str:
    """Get a 5-day weather forecast for a European city.

    Args:
        city: City name (e.g. Paris, Berlin, Rome)
        country_code: Optional ISO 3166-1 alpha-2 country code to disambiguate (e.g. FR, DE, IT)
    """
    location = await resolve_city(city, country_code)
    if not location:
        hint = f" Try adding country_code (e.g. FR for {city})." if not country_code else ""
        return f"Could not find city '{city}'.{hint}"

    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max",
        "timezone": "auto",
        "forecast_days": 5,
    }
    data = await api_get(FORECAST_API, params)
    if not data or "daily" not in data:
        return f"Unable to fetch forecast for {location_label(location)}."

    daily = data["daily"]
    periods: list[str] = []
    label = location_label(location)

    for i, date in enumerate(daily["time"]):
        code = daily["weathercode"][i]
        period = f"""
{date}:
Conditions: {weather_description(code)}
Temperature: {daily['temperature_2m_min'][i]:.0f}°C – {daily['temperature_2m_max'][i]:.0f}°C
Precipitation: {daily['precipitation_sum'][i]} mm
Max wind: {daily['windspeed_10m_max'][i]} km/h
"""
        periods.append(period.strip())

    return f"5-day forecast for {label}:\n\n" + "\n---\n".join(periods)


def main():
    # using stdio transport for local testing
    # mcp.run(transport="stdio")

    # using streamable HTTP transport for remote testing
    # FastMCP handles all the web server configuration for you
    mcp.run(transport="http", host="0.0.0.0", port=8000)




if __name__ == "__main__":
    main()
