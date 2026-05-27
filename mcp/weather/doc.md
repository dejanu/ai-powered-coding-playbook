* Start "wheather" MCP server

```
uv --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER/weather run weather.py
```

* Update Claude Desktop settings

```
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/demo",
        "run",
        "weather.py"
      ]
    }
  }
}




MCP endpoint: `http://localhost:8000/mcp`