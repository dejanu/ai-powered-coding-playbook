* Start "wheather" MCP server

```
uv --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER/weather run weather.py

uv sync
uv run fastmcp run weather.py:mcp

# debug mcp server
uv run fastmcp dev inspector weather.py
uv run mcp dev weather.py
```

* Update Claude Desktop settings (safe to place it unde `~` for STDIO)

```
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/weather",
        "run",
        "weather.py"
      ]
    }
  }
}
```



MCP endpoint: `http://localhost:8000/mcp`

# send a JSON-RPC 2.0 initialize request to the MCP server over HTT
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -D - \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"curl-test","version":"1.0"}}}'


# list tools
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 546bb2f58cbf41269ebf79803d17fcd3" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'

curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 546bb2f58cbf41269ebf79803d17fcd3" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_forecast","arguments":{"city":"Rome","country_code":"IT"}}}'