## MCP folder overview

This folder contains hands-on Python examples for building and running MCP-based tools and clients.

- `cli_project/`
  - A command-line MCP chat app wired to Anthropic.
  - Includes an MCP server (`mcp_server.py`) and client (`mcp_client.py`).
  - `core/` holds chat, CLI, and tool wiring modules.
  - `README.md` explains setup, usage (`@document`, `/command`), and local development flow.

- `fastmcp_demo/`
  - A lightweight FastMCP example showing client/server interaction.
  - Includes `my_server.py`, `my_client.py`, and `main.py`.
  - `readme.md` documents both direct stdio usage and host-based usage (for example, via VS Code), plus MCP vs FastMCP notes.

- `weather/`
  - A FastMCP server that exposes city weather data via the free Open-Meteo API (no API key).
  - `weather.py` defines two tools: `get_forecast` (5-day daily forecast) and `get_weather_advisories` (3-day rule-based alerts for rain, wind, heat, cold, and thunderstorms).
  - Resolves city names to coordinates with optional `country_code` disambiguation (e.g. `FR`, `IT`).
  - Runs over HTTP by default (`http://localhost:8000/mcp`); stdio is available by switching the transport in `main()`.
  - `doc.md` covers startup commands (`uv run weather.py`, MCP Inspector), Claude Desktop config, and curl examples.

- Shared project files
  - `pyproject.toml` and `uv.lock` appear in each example for dependency and environment management.
  - `.gitignore` excludes virtual envs, caches, build artifacts, logs, and local secrets.
